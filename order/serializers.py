from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import *
from product.serializers import ProductVariantLineItemSerializer


class LineItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = LineItem
        fields = '__all__'
        depth = 0


class LineItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LineItem
        fields = ['id', 'product_variant', 'count']
        read_only_fields = ['id']
        depth = 0

    def create(self, validated_data):
        request = self.context.get("request", None)

        # Checking if product variant is available to purchase
        product_variant = validated_data.get('product_variant', None)
        if not product_variant or not (product_variant.current and product_variant.approved):
            raise ValidationError({"message": "There is no such an available product variant to purchase"})

        # Checking if an order with a null purchase date already exists
        order = Order.objects.filter(user=request.user, purchase_date__isnull=True).first()
        if not order:
            order = Order(user=request.user)
            order.save()

        # Checking if product variant is already in the basket
        # If so don't create new one, just update the count of the existing
        line_item_of_variant = order.lines.filter(product_variant=validated_data.get('product_variant')).first()
        if line_item_of_variant:
            new_count = line_item_of_variant.count + validated_data.get('count')
            serializer = LineItemUpdateCountSerializer(line_item_of_variant, data={'count': new_count}, context={'request': request})
            serializer.is_valid(raise_exception=True)
            line_item = serializer.save()
        else:
            validated_data.update({'order': order})
            line_item = LineItem.objects.create(**validated_data)

        return line_item


class LineItemUpdateCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = LineItem
        fields = ['count']
        depth = 0

    def validate(self, data):
        request = self.context.get("request", None)

        if self.instance.order.user != request.user:
            raise ValidationError({"message": "You are not allowed to do this."})

        return data


class LineItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LineItem
        fields = ['count']
        depth = 0


class LineItemListSerializer(serializers.ModelSerializer):
    cost = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    product_variant = ProductVariantLineItemSerializer()

    def get_price(self, obj):
        return obj.product_variant.price

    def get_cost(self, obj):
        return obj.product_variant.price * obj.count

    class Meta:
        model = LineItem
        fields = ['id', 'product_variant', 'price', 'count', 'cost']
        depth = 0


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        depth = 0


class OrderPurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['purchase_date']
        depth = 0

    def validate(self, data):
        if data.get('purchase_date', None):
            raise ValidationError({"message": _("Order Purchase Error: Already purchased")})

        data.update({'purchase_date': timezone.now()})

        return data


class OrderListSerializer(serializers.ModelSerializer):
    line_items = LineItemListSerializer(many=True)
    total_cost = serializers.SerializerMethodField()

    def get_total_cost(self, obj):
        total_cost = 0
        for line_item in obj.lines.all():
            total_cost += line_item.product_variant.price * line_item.count
        return total_cost

    class Meta:
        model = Order
        fields = ['id', 'total_cost', 'purchase_date', 'line_items']
        depth = 0


class OrderBasketSerializer(serializers.ModelSerializer):
    total_cost = serializers.SerializerMethodField()
    line_items = LineItemListSerializer(many=True)
    # products = serializers.SerializerMethodField()
    #
    # def get_products(self, obj):
    #     ProductBasketSerializer(context={'order': obj})

    def get_total_cost(self, obj):
        total_cost = 0
        for line_item in obj.lines.all():
            total_cost += line_item.product_variant.price * line_item.count
        return total_cost

    class Meta:
        model = Order
        fields = ['total_cost', 'line_items']
        depth = 0