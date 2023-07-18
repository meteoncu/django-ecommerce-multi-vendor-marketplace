from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('line', views.LineItemViewSet, basename='line')
router.register('', views.OrderViewSet, basename='order')

app_name = 'order'

urlpatterns = [
    path("", include(router.urls)),
]
