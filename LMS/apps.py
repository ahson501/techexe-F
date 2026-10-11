from django.apps import AppConfig


class LmsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'LMS'  # Ensure this matches your app's directory name

    def ready(self):
        import LMS.signals  # Signal handlers imported when app is ready
