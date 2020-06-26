import json

from rest_framework import serializers
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from .models import Task
from .search_indexes import TaskDocument


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class TaskDocumentSerializer(DocumentSerializer):
    class Meta:
        model = Task
        document = TaskDocument
        fields = ('title', 'description', 'author', 'assigned', 'status', 'is_started')
