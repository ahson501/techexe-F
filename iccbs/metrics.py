# iccbs/metrics.py
from django.http import HttpResponse
from iccbs.models import SNMPTrap
from iccbs.mibs_map import SANGFOR_MIB_MAP

def metrics_view(request):
    """
    Expose metrics in Prometheus format (plain text)
    """
    traps = SNMPTrap.objects.all().order_by('-timestamp')[:50]

    metrics_output = []
    metrics_output.append("# HELP sangfor_snmp_traps_total Total number of received SNMP traps")
    metrics_output.append("# TYPE sangfor_snmp_traps_total counter")
    metrics_output.append(f"sangfor_snmp_traps_total {traps.count()}")

    # Count per OID
    metrics_output.append("\n# HELP sangfor_snmp_trap_oid_total Number of traps per OID")
    metrics_output.append("# TYPE sangfor_snmp_trap_oid_total counter")

    oid_counts = {}
    for trap in traps:
        oid_counts[trap.trap_oid] = oid_counts.get(trap.trap_oid, 0) + 1

    for oid, count in oid_counts.items():
        name = SANGFOR_MIB_MAP.get(oid, "unknown")
        metrics_output.append(f'sangfor_snmp_trap_oid_total{{oid="{oid}",name="{name}"}} {count}')

    # Severity level count
    metrics_output.append("\n# HELP sangfor_snmp_trap_severity_total Number of traps by severity")
    metrics_output.append("# TYPE sangfor_snmp_trap_severity_total counter")
    severity_counts = {"info": 0, "warning": 0, "critical": 0}

    for trap in traps:
        severity_counts[trap.severity] = severity_counts.get(trap.severity, 0) + 1

    for sev, count in severity_counts.items():
        metrics_output.append(f'sangfor_snmp_trap_severity_total{{severity="{sev}"}} {count}')

    # Return as Prometheus format
    return HttpResponse("\n".join(metrics_output), content_type="text/plain")
