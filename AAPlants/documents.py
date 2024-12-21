from django_elasticsearch_dsl import Document, Text, Keyword, Date, Integer
from django_elasticsearch_dsl.registries import registry
from .models import Plant

@registry.register_document
class PlantDocument(Document):
    name = Text()
    scientific_name = Text()
    description = Text()
    care_instructions = Text()
    available = Keyword()
    created_at = Date()
    updated_at = Date()
    category = Keyword()

    class Index:
        name = 'plants'  # Name of the Elasticsearch index
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0
        }

    class Django:
        model = Plant  # The model associated with this Document
        fields = []  # Leave empty as fields are explicitly defined above

