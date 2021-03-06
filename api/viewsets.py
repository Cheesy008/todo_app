from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .tasks import send_email_task

from main.models import Task
from .serializers import (
    TaskDetailSerializer,
    TaskListSerializer,
    TaskCreateSerializer,
)

class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer
    serializer_action_classes = {
        'list': TaskListSerializer,
        'create': TaskCreateSerializer,
    }

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

    def perform_update(self, serializer):
        instance = serializer.save()
        user_email = self.request.user.email
        if instance.is_done:
            send_email_task.delay(user_email, 'Выполнено')
        else:
            send_email_task.delay(user_email, 'Не выполнено')

    @action(detail=True, methods=['get', 'post'], serializer_class=TaskDetailSerializer)
    def execute(self, request, pk=None):
        Task.objects.filter(pk=pk).update(is_done=True)
        user_email = request.user.email
        send_email_task.delay(user_email, 'Выполнено')
        return Response(status=status.HTTP_200_OK)
