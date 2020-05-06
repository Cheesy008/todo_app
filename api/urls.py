from rest_framework.routers import DefaultRouter

from .viewsets import (
    TaskViewSet,
)

router = DefaultRouter()
router.register('todo', TaskViewSet, basename='todo')

urlpatterns = router.urls

