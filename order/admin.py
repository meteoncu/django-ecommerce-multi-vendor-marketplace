from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter
from django_admin_inline_paginator.admin import TabularInlinePaginated
from .models import *


class LineItemInline(admin.TabularInline):
    model = LineItem
    fields = ['product_listing', 'price', 'count', 'cost', 'created_at']
    readonly_fields = fields
    can_delete = False
    show_change_link = False
    extra = 0
    max_num = 0

    def price(self, obj):
        return obj.product_listing.price

    def cost(self, obj):
        return obj.product_listing.price * obj.count


@admin.register(Order)
class OrderAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ("id", "user", "lines_count", "product_count", "cost", "purchased_at",)
    readonly_fields = list_display
    search_fields = ['user__email', 'lines__product_listing__product_variant__name', 'lines__product_listing__product_variant__name']
    list_filter = (
        ('purchased_at', DateRangeFilter),
    )

    fieldsets = (
        ('INFORMATION', {
            'fields': ("id", "user", "purchased_at",),
        }),
    )

    inlines = [
        LineItemInline,
    ]

    def lines_count(self, obj):
        return obj.lines.count()

    def product_count(self, obj):
        number = 0
        for line_item in obj.lines.all():
            number += line_item.count
        return number

    def cost(self, obj):
        total_cost = 0
        for line_item in obj.lines.all():
            total_cost += line_item.products_listing.price * line_item.count
        return total_cost

    def get_rangefilter_create_date_title(self, request, field_path):
        return 'By create date'

    def get_rangefilter_update_date_title(self, request, field_path):
        return 'By update date'

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        qs = super(OrderAdmin, self).get_queryset(request)
        qs = qs.filter(purchase_date__isnull=False)
        return qs


@admin.register(LineItem)
class LineItemAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ("id", "user", "product", "product_listing", "price", "count", "cost")
    search_fields = ["order__user__email", "product_listing__product_variant__product__category__name", "product_listing__product_variant__name", "product_listing__product_variant__product__name"]

    def user(self, obj):
        return obj.order.user

    def price(self, obj):
        return obj.product_listing.product_variant.price

    def cost(self, obj):
        return obj.product_listing.product_variant.price * obj.count

    def product(self, obj):
        return obj.product_listing.product_variant.product

    def product_variant(self, obj):
        return obj.product_listing.product_variant

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        qs = super(LineItemAdmin, self).get_queryset(request)
        qs = qs.filter(order__purchased_at__isnull=True).order_by("order__user__id")
        return qs
