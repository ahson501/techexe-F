from django.core.management.base import BaseCommand
from AAPlants.models import Plant
from AAPlants.documents import PlantDocument

class Command(BaseCommand):
    help = "Index existing Plant data to Elasticsearch"

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting to index Plant data...")
        for plant in Plant.objects.all():
            doc = PlantDocument(
                meta={"id": plant.id},
                name=plant.name,
                scientific_name=plant.scientific_name,
                description=plant.description,
                care_instructions=plant.care_instructions,
                category=plant.category.name,
            )
            doc.save()
            self.stdout.write(f"Indexed Plant: {plant.name}")
        self.stdout.write("Finished indexing Plant data.")
