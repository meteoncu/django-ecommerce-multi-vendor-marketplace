from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('', views.UserViewSet, basename='user')

app_name = 'user'

urlpatterns = [
    path("", include(router.urls)),
]
