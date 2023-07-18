from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import *
from .permissions import IsOrderOwner, IsLineItemOwner, IsLineItemNotPurchased
from user.permissions import IsAdmin
from .models import *


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'list':
            return OrderListSerializer
        elif self.action == 'purchase':
            return OrderPurchaseSerializer
        else:
            return OrderSerializer

    def get_permissions(self):
        if self.action == 'basket' or self.action == 'purchase' or self.action == 'buyers' or self.action == 'sellers'\
                or self.action == 'empty_basket':
            permission_classes = [IsAuthenticated]
        elif self.action == 'retrieve':
            permission_classes = [IsOrderOwner]
        elif self.action == 'list' or self.action == 'all':
            permission_classes = [IsAdmin]
        else:
            # Create, destroy, update
            permission_classes = [~AllowAny]
        return [permission() for permission in permission_classes]

    def get_serializer_context(self):
        context = super(OrderViewSet, self).get_serializer_context()
        context.update({"request": self.request})
        return context

    @action(detail=False, methods=['GET'], name='sellers')
    def sellers(self, request, *args, **kwargs):
        queryset = Order.objects.filter(lines__product_listing__product__user=request.user, purchase_date__isnull=False)
        page = self.paginate_queryset(queryset)
        return Response(OrderListSerializer(page, many=True).data, status=200)

    @action(detail=False, methods=['GET'], name='buyers')
    def buyers(self, request, *args, **kwargs):
        queryset = Order.objects.filter(user=request.user, purchase_date__isnull=False)
        page = self.paginate_queryset(queryset)
        return Response(OrderListSerializer(page, many=True).data, status=200)

    @action(detail=False, methods=['GET'], name='basket')
    def basket(self, request, *args, **kwargs):
        order = Order.objects.filter(user=request.user, purchase_date__isnull=True).first()
        if not order:
            order = Order(user=request.user)
        return Response(OrderBasketSerializer(order).data, status=200)

    @action(detail=False, methods=['DELETE'], name='empty_basket')
    def empty_basket(self, request, *args, **kwargs):
        order = Order.objects.filter(user=request.user, purchase_date__isnull=True).first()
        if order:
            order.delete()
        return Response({"message": "Basket is empty"}, status=200)

    @action(detail=False, methods=['GET'], name='purchase')
    def purchase(self, request, *args, **kwargs):
        order = Order.objects.filter(user=self.request.user, purchase_date__isnull=True).first()
        if not order:
            return Response({"message": "Not found"}, status=404)

        serializer = OrderPurchaseSerializer(order, data={})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(OrderListSerializer(order).data, status=200)

    @action(detail=False, methods=['DELETE'], name='all')
    def all(self, request, *args, **kwargs):
        Order.objects.all().delete()
        return Response({"message": "Deleted successfully"}, status=200)


class LineItemViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = LineItemViewSet.objects.filter(order__user=self.request.user, order__purchase_date__isnull=True)
        return queryset

    def get_serializer_class(self):
        if self.action == 'create':
            return LineItemCreateSerializer
        elif self.action == 'retrieve' or self.action == 'list':
            return LineItemListSerializer
        elif self.action == 'update':
            return LineItemUpdateCountSerializer
        else:
            return LineItemSerializer

    def get_permissions(self):
        if self.action == 'create' or self.action == 'list':
            permission_classes = [IsAuthenticated]
        elif self.action == 'retrieve':
            permission_classes = [IsLineItemOwner]
        elif self.action == 'update' or self.action == 'destroy':
            permission_classes = [IsLineItemOwner, IsLineItemNotPurchased]
        else:
            permission_classes = [~AllowAny]
        return [permission() for permission in permission_classes]

    def get_serializer_context(self):
        context = super(LineItemViewSet, self).get_serializer_context()
        context.update({"request": self.request})
        return context
