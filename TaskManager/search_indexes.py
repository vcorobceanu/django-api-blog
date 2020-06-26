from django.conf import settings
from django_elasticsearch_dsl import Document, Index, fields
from elasticsearch_dsl import analyzer
from django.contrib.auth.models import User

from .models import Task

INDEX = Index(settings.ELASTICSEARCH_INDEX_NAMES[__name__])

INDEX.settings(
    number_of_shards=1,
    number_of_replicas=1
)

html_strip = analyzer(
    'html_strip',
    tokenizer="standard",
    filter=["standard", "lowercase", "stop", "snowball"],
    char_filter=["html_strip"]
)


class TaskDocument(Document):
    """Task Elasticsearch document."""

    title = fields.TextField(
        analyzer=html_strip,
        fields={
            'raw': fields.TextField(analyzer='keyword'),
        }
    )

    description = fields.TextField(
        analyzer=html_strip,
        fields={
            'raw': fields.TextField(analyzer='keyword'),
        }
    )

    author = fields.ObjectField(properties={
        'username': fields.TextField(analyzer=html_strip)
    })

    assigned = fields.ObjectField(properties={
        'username': fields.TextField(analyzer=html_strip)
    })

    status = fields.BooleanField(attr='status_indexing')
    is_started = fields.BooleanField(attr='is_started_indexing')

    class Django(object):
        """Inner nested class Django."""

        model = Task  # The model associate with this Document
        related_models = [User]

    # def get_queryset(self):
    #     """Not mandatory but to improve performance we can select related in one sql request"""
    #     return super(TaskDocument, self).get_queryset().select_related(
    #         'User'
    #     )
    #
    # def get_instances_from_related(self, related_instance):
    #     """If related_models is set, define how to retrieve the Car instance(s) from the related model.
    #     The related_models option should be used with caution because it can lead in the index
    #     to the updating of a lot of items.
    #     """
    #     if isinstance(related_instance, User):
    #         return related_instance.Task