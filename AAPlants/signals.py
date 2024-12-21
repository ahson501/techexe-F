from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Plant
from .documents import PlantDocument

@receiver(post_save, sender=Plant)
def index_plant(sender, instance, **kwargs):
    doc = PlantDocument(
        meta={"id": instance.id},
        name=instance.name,
        scientific_name=instance.scientific_name,
        description=instance.description,
        care_instructions=instance.care_instructions,
        category=instance.category.name,
    )
    doc.save()

@receiver(post_delete, sender=Plant)
def delete_plant(sender, instance, **kwargs):
    PlantDocument(meta={"id": instance.id}).delete()
