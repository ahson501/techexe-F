#!/usr/bin/env python3
import sys
import logging
from pysnmp.hlapi.v3arch.asyncio import SnmpEngine
from pysnmp.entity import config
from pysnmp.carrier.asyncio.dgram import udp
from pysnmp.entity.rfc3413 import ntfrcv
from prometheus_client import start_http_server, Gauge

# === Logging setup ===
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# === Prometheus metrics ===
link_status_gauge = Gauge(
    'link_status',
    'Link status (1=up, 0=down) per interface',
    ['interface']
)

bandwidth_util_gauge = Gauge(
    'bandwidth_utilization_percent',
    'Estimated bandwidth utilization percentage per interface',
    ['interface']
)

# === SNMP Engine ===
snmp_engine = SnmpEngine()

# SNMPv3 credentials
SECURITY_USER = "ICCBS_Network_Alert_Trap"
AUTH_KEY = "1kapadia"
PRIV_KEY = "1kapadia"

config.add_v3_user(
    snmp_engine,
    SECURITY_USER,
    config.USM_AUTH_HMAC96_SHA,
    AUTH_KEY,
    config.USM_PRIV_CFB128_AES,
    PRIV_KEY
)

# === Transport setup (UDP 10162) ===
LISTEN_IP = "0.0.0.0"
LISTEN_PORT = 10162

transport = udp.UdpTransport().open_server_mode((LISTEN_IP, LISTEN_PORT))
config.add_transport(snmp_engine, udp.DOMAIN_NAME, transport)

logging.info(f"✅ SNMP Trap Receiver listening on UDP {LISTEN_IP}:{LISTEN_PORT}")

# === Trap Handler ===
def trap_callback(snmp_engine, state_reference, context_engine_id, context_name, var_binds, cb_ctx):
    logging.info("📩 SNMP Trap received.")
    interface_name = "unknown"
    link_status = None
    bandwidth_util = None

    for name, val in var_binds:
        oid_str = str(name)
        value_str = str(val)
        logging.info(f"VarBind: {oid_str} = {value_str}")

        # IF-MIB OIDs
        if "1.3.6.1.2.1.2.2.1.2" in oid_str:  # ifDescr
            interface_name = value_str
        elif "1.3.6.1.2.1.2.2.1.8" in oid_str:  # ifOperStatus
            link_status = 1 if int(value_str) == 1 else 0
        elif "1.3.6.1.2.1.31.1.1.1.10" in oid_str:  # ifHCOutOctets
            bandwidth_util = min((int(value_str) / 10000000) * 100, 100)

    # Update Prometheus metrics
    if interface_name != "unknown":
        if link_status is not None:
            link_status_gauge.labels(interface=interface_name).set(link_status)
        if bandwidth_util is not None:
            bandwidth_util_gauge.labels(interface=interface_name).set(bandwidth_util)

    logging.info(f"📊 Updated metrics for {interface_name}: link={link_status}, bw={bandwidth_util}")

# Register SNMP Trap callback
ntfrcv.NotificationReceiver(snmp_engine, trap_callback)

# === Prometheus endpoint ===
PROMETHEUS_PORT = 8001
start_http_server(PROMETHEUS_PORT)
logging.info(f"🌐 Prometheus metrics available at http://0.0.0.0:{PROMETHEUS_PORT}/metrics")

# === Dispatcher (sync run loop) ===
try:
    snmp_engine.transport_dispatcher.job_started(1)
    snmp_engine.transport_dispatcher.run_dispatcher()
except KeyboardInterrupt:
    logging.info("🛑 Interrupted by user, shutting down gracefully.")
    snmp_engine.transport_dispatcher.close_dispatcher()
    sys.exit(0)
