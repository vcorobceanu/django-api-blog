from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_elasticsearch.es_serializer import ElasticModelSerializer
from .models import Task
from .search_indexes import TaskIndex
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class ElasticBlogSerializer(ElasticModelSerializer):
    class Meta:
        model = Task
        es_model = TaskIndex
        fields = ('title', 'description', 'author', 'assigned', 'status', 'is_started')
