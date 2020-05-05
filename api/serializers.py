from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from main.models import Task


class CustomTokenSerializer(serializers.Serializer):
    token = serializers.CharField()


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
