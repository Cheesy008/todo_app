from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from main.models import Task


class TaskCreateSerializer(ModelSerializer):
    class Meta:
        model = Task
        exclude = ('is_done',)


class TaskListSerializer(ModelSerializer):
    class Meta:
        model = Task
        exclude = ('content',)


class TaskDetailSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
