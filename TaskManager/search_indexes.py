from elasticsearch   import (
    DocType,
    Date,
    Keyword,
    Text,
    Boolean,
    Integer
)


class TaskIndex(DocType):
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