from django.apps import AppConfig


class AAPlantsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'AAPlants'

def ready(self):
        import AAPlants.documents  # Ensure the documents are loaded




    