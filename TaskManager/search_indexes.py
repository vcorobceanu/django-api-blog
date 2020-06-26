from django_elasticsearch_dsl import (
    DocType,
    Date,
    Keyword,
    Text,
    Boolean,
    Integer,
    Index
)
from .models import Task
task = Index('Task')

@task.doc_type
class TaskDocument(DocType):
    """
    TaskIndex.init(using=es_client)
    """
    title = Keyword()
    description = Text(fields={'raw': Keyword()})
    author = Text()
    assigned = Text()
    status = Keyword(multi=True)
    is_started = Boolean()

    class Meta:
        index = 'Task'
