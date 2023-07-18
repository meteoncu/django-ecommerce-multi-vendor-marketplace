from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from user.permissions import IsAdmin
from .permissions import *
from .serializers import *
from .models import *


class ProductViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = Product.objects.all()
        # if self.action == 'list':
        #     queryset = Product.objects.filter(user=self.request.user).order_by("-create_date")
        # else:
        #     queryset = Product.objects.filter(user=self.request.user).order_by("-create_date")
        return queryset

    def get_serializer_class(self):
        if self.action == 'create':
            return ProductCreateSerializer
        elif self.action == 'retrieve' or self.action == 'list':
            return ProductDetailedSerializer
        elif self.action == 'update':
            return ProductUpdateSerializer
        elif self.action == 'direct_update':
            return ProductDirectUpdateSerializer
        else:
            return ProductSerializer

    def get_serializer_context(self):
        context = super(ProductViewSet, self).get_serializer_context()
        context.update({"request": self.request})
        return context

    def get_permissions(self):
        if self.action == 'create' or self.action == 'my':
            permission_classes = [IsAuthenticated]
        elif self.action == 'retrieve' or self.action == 'update':
            permission_classes = [IsProductOwnerOrAdmin]
        elif self.action == 'list_initial_rejected' or self.action == 'list_initial_approval' or \
                self.action == 'list_change_approval' or self.action == 'approve_initially' or \
                self.action == 'reject_initially' or self.action == 'approve_changes' or \
                self.action == 'reject_changes' or self.action == 'list' or self.action == 'all':
            permission_classes = [IsAdmin]
        elif self.action == 'direct_update':
            permission_classes = [DirectUpdatePermission]
        else:
            permission_classes = [~AllowAny]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['PATCH'], name='direct_update')
    def direct_update(self, request, *args, **kwargs):
        product = self.get_object()

        serializer = ProductDirectUpdateSerializer(product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=200)

    @action(detail=False, methods=['GET'], name='my')
    def my(self, request, *args, **kwargs):
        queryset = Product.objects.filter(user=request.user).order_by('-id')
        page = self.paginate_queryset(queryset)
        return Response(ProductDetailedSerializer(page, many=True).data, status=200)

    @action(detail=False, methods=['GET'], name='list_initial_rejected')
    def list_initial_rejected(self, request, *args, **kwargs):
        queryset = Product.objects.filter(approved=False)
        page = self.paginate_queryset(queryset)
        return Response(ProductListSerializer(page, many=True).data, status=200)

    @action(detail=False, methods=['GET'], name='list_initial_approval')
    def list_initial_approval(self, request, *args, **kwargs):
        queryset = Product.objects.filter(approved=None)
        page = self.paginate_queryset(queryset)
        return Response(ProductListSerializer(page, many=True).data, status=200)

    @action(detail=False, methods=['GET'], name='list_change_approval')
    def list_change_approval(self, request, *args, **kwargs):
        queryset = ProductDraft.objects.all()
        page = self.paginate_queryset(queryset)
        serializer = ProductUpdatedListSerializer(page, many=True, context={'request': request})
        return Response(serializer.data, status=200)

    @action(detail=True, methods=['POST'], name='approve_initially')
    def approve_initially(self, request, *args, **kwargs):
        product = self.get_object()
        product.approved = True
        product.save()
        return Response(ProductListSerializer(product).data, status=200)

    @action(detail=True, methods=['DELETE'], name='reject_initially')
    def reject_initially(self, request, *args, **kwargs):
        product = self.get_object()
        product.approved = False
        product.save()
        return Response(ProductListSerializer(product).data, status=200)

    @action(detail=True, methods=['POST'], name='approve_changes')
    def approve_changes(self, request, *args, **kwargs):
        product = self.get_object()
        draft = product.drafts.first()

        if not draft:
            raise ValidationError({"message": "There is no changes for this product"})

        # Applying inner changes onto the product
        data = ProductDraftSerializer(draft).data
        data.pop('original')
        serializer = ProductSerializer(product, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Setting M2M objects
        product.feature_options.set(draft.feature_options.all())

        # Removing draft
        draft.delete()

        new_variants = product.variants.filter(current=True, approved=None)
        if new_variants.count() > 0:
            # Making old variants invisible, they need to be kept
            product.variants.filter(current=True, approved=True).update(current=False)

            # Making new variants approved
            new_variants.update(approved=True)

        # Approving new images
        product.images.filter(approved=None).update(approved=True)

        # Deleting requested images
        product.images.filter(delete=True).delete()

        return Response(ProductListSerializer(product).data, status=200)

    @action(detail=True, methods=['DELETE'], name='reject_changes')
    def reject_changes(self, request, *args, **kwargs):
        product = self.get_object()
        draft = product.drafts.first()
        if not draft:
            raise ValidationError({"message": "There is no changes for this product"})

        # Deleting new variants
        product.variants.filter(current=True, approved=None).delete()

        # Deleting new images
        product.images.filter(approved=None).delete()

        # Removing delete request of images
        product.images.filter(delete=True).update(delete=False)

        # Deleting draft object
        draft.delete()

        return Response(ProductListSerializer(product).data, status=200)

    @action(detail=False, methods=['DELETE'], name='all')
    def all(self, request, *args, **kwargs):
        Product.objects.all().delete()
        return Response({"message": "Deleted successfully"}, status=200)


class ProductVariantViewSet(viewsets.ModelViewSet):
    queryset = ProductVariant.objects.all()

    def get_serializer_class(self):
        if self.action == 'inventory_update':
            return ProductVariantInventorySerializer
        else:
            return ProductVariantSerializer

    def get_serializer_context(self):
        context = super(ProductVariantViewSet, self).get_serializer_context()
        context.update({"request": self.request})
        return context

    def get_permissions(self):
        if self.action == 'inventory_update':
            permission_classes = [IsProductVariantOwner]
        else:
            permission_classes = [~IsAdmin]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['PATCH'], name='inventory_update')
    def inventory_update(self, request, *args, **kwargs):
        product_variant = self.get_object()

        serializer = ProductVariantInventorySerializer(product_variant, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=200)


class CategoryViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        if self.action == 'list':
            queryset = Category.objects.filter(parent__isnull=True)
        else:
            queryset = Category.objects.all()
        return queryset

    def get_serializer_class(self):
        if self.action == 'create':
            return CategoryCreateSerializer
        elif self.action == 'retrieve':
            return CategoryRetrieveSerializer
        elif self.action == 'list':
            return CategoryListSerializer
        else:
            return CategorySerializer

    def get_serializer_context(self):
        context = super(CategoryViewSet, self).get_serializer_context()
        context.update({"request": self.request})
        return context

    def get_permissions(self):
        if self.action == "retrieve" or self.action == "list":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdmin]
        return [permission() for permission in permission_classes]
