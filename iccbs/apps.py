from django.apps import AppConfig

class IccbsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'iccbs'

def ready(self):
    import iccbs.signals
    from .snmp_trap_receiver import start_snmp_trap_server
    start_snmp_trap_server()
    