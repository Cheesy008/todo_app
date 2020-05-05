from rest_framework.routers import DefaultRouter
from django.urls import path

from .views import (
    TaskViewSet,
    CustomPasswordTokenVerificationView,
)

router = DefaultRouter()
router.register('todo', TaskViewSet, basename='todo')

urlpatterns = [
    path('reset-password/verify-token/', CustomPasswordTokenVerificationView.as_view(),
         name='password_reset_verify_token'),

]

urlpatterns += router.urls

