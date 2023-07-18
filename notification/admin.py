from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter
from django_admin_inline_paginator.admin import TabularInlinePaginated
from .models import *


@admin.register(Notification)
class NotificationAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ("type", "user", "notified_by", "message", "is_read", "created_at")
    list_filter = (
        "type", "user", "notified_by", "is_read",
        ('created_at', DateRangeFilter),
    )

    def get_rangefilter_created_at_title(self, request, field_path):
        return 'By create date'

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
