from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry

from .models import TestQuiz


@registry.register_document
class TestQuizDocument(Document):

    class Index:
        name = 'tests_quiz'
        settings = {'number_of_shards': 1, 'number_of_replicas': 0}

    class Django:
        model = TestQuiz

        fields = [
            'id',
            'name',
            'description',
        ]