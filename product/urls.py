from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('category', views.CategoryViewSet, basename='category')
router.register('product_variant', views.ProductVariantViewSet, basename='product_variant')
router.register('', views.ProductViewSet, basename='product')

app_name = 'product'

urlpatterns = [
    path("", include(router.urls)),
]
