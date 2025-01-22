# iccbs/apps.py
from django.apps import AppConfig

class iccbsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'iccbs'

    def ready(self):
        import iccbs.signals
