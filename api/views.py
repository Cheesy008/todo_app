from datetime import timedelta
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django_rest_passwordreset.models import ResetPasswordToken, get_password_reset_token_expiry_time
from django_rest_passwordreset.signals import reset_password_token_created
from rest_framework import viewsets, status, parsers, renderers
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.urls import reverse

from .tasks import send_email_task

from main.models import Task
from .serializers import (
    TaskDetailSerializer,
    TaskListSerializer,
    TaskCreateSerializer,
)


class CustomPasswordResetView:
    @receiver(reset_password_token_created)
    def password_reset_token_created(sender, reset_password_token, *args, **kwargs):
        context = {
            'current_user': reset_password_token.user,
            'username': reset_password_token.user.username,
            'email': reset_password_token.user.email,
            'reset_password_url': "{}?token={}".format(reverse('password_reset:reset-password-request'),
                                                       reset_password_token.key),
            'site_name': 'example.com',
            'site_domain': 'example.com'
        }

        email_html_message = render_to_string('email/user_reset_password.html', context)
        email_plaintext_message = render_to_string('email/user_reset_password.txt', context)

        msg = EmailMultiAlternatives(
            "Password Reset for {}".format('example.com'),
            email_plaintext_message,
            "mrworld008@gmail.com",
            [reset_password_token.user.email]
        )
        msg.attach_alternative(email_html_message, "text/html")
        msg.send()


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

    @action(detail=True, methods=['get', 'post'], serializer_class=TaskDetailSerializer)
    def execute(self, request, pk=None):
        Task.objects.filter(pk=pk).update(is_done=True)
        # send_email_task.delay()
        return Response(status=status.HTTP_200_OK)
