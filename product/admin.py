from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter
from django.contrib.admin import SimpleListFilter
from django_admin_inline_paginator.admin import TabularInlinePaginated
from .models import *
from django.utils.translation import gettext as _
from django import forms


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    fields = ["id", "image"]
    readonly_fields = fields
    # readonly_fields = ["id"]
    can_delete = False
    show_change_link = False
    extra = 0
    max_num = 0


class DraftInline(admin.TabularInline):
    model = ProductDraft
    fields = ["name", "category", "description"]
    readonly_fields = fields
    can_delete = False
    show_change_link = False
    extra = 0
    max_num = 0


class CategoryInline(admin.TabularInline):
    model = Category
    fields = ["id", "name", "parent"]
    readonly_fields = fields
    can_delete = False
    show_change_link = False
    extra = 0
    max_num = 0


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    fields = ("id", "product", "name", "description", "inventory", "approved")
    readonly_fields = fields
    can_delete = False
    show_change_link = False
    extra = 0
    max_num = 0


class ProductInline(admin.TabularInline):
    model = Product
    fields = ["id", "user", "name", "description"]
    readonly_fields = fields
    can_delete = False
    show_change_link = False
    extra = 0
    max_num = 0


class FeatureValueInline(admin.TabularInline):
    model = FeatureValue
    fields = ["id", "product", "name"]
    readonly_fields = ["id", "feature", "product"]
    can_delete = True
    show_change_link = True
    extra = 0
    max_num = 0

    def get_queryset(self, request):
        qs = super(FeatureValueInline, self).get_queryset(request)
        return qs.order_by('id')


class FeatureValueProductInline(admin.TabularInline):
    model = FeatureValue
    fields = ["id", "feature", "product", "name"]
    readonly_fields = fields
    # readonly_fields = ["id"]
    can_delete = False
    show_change_link = True
    extra = 0
    max_num = 0

    def get_queryset(self, request):
        qs = super(FeatureValueProductInline, self).get_queryset(request)
        return qs.order_by('id')


class DraftExistsListFilter(admin.SimpleListFilter):
    title = _('Has changes')
    parameter_name = 'has_changes'

    def lookups(self, request, model_admin):
        return (
            ('yes', _('Yes')),
            ('no',  _('No')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(drafts__isnull=False)
        if self.value() == 'no':
            return queryset.filter(drafts__isnull=True)
        return queryset


class MainCategoryListFilter(admin.SimpleListFilter):
    title = _('Main Category')
    parameter_name = 'main_category'

    def lookups(self, request, model_admin):
        return (
            ('yes', _('Yes')),
            ('no',  _('No')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(parent__isnull=True)
        if self.value() == 'no':
            return queryset.filter(parent__isnull=False)
        return queryset


class ProductFeatureOptionInlineForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductFeatureOptionInlineForm, self).__init__(*args, **kwargs)
        if self.instance.id:
            self.fields['featureoption'].queryset = FeatureOption.objects.filter(feature=self.instance.featureoption.feature).order_by("id")
        # else:
        #     self.fields['featureoption'].queryset = FeatureOption.objects.all().exclude(feature__in=self.instance.product.feature_options).order_by("id")


class ProductFeatureOptionInline(admin.TabularInline):
    model = Product.feature_options.through
    can_delete = False
    show_change_link = False
    extra = 0
    max_num = 0
    form = ProductFeatureOptionInlineForm


class ProductDraftFeatureOptionInline(admin.TabularInline):
    model = ProductDraft.feature_options.through
    can_delete = False
    show_change_link = False
    extra = 0
    max_num = 0


@admin.register(Product)
class ProductAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ["id", "category", "name", "description", "user", "approved", "changed", "create_date"]
    readonly_fields = list_display + ["update_date"]
    actions = ['initial_approve', 'initial_reject']
    search_fields = ['user__email']
    list_filter = (
        'category', 'approved', DraftExistsListFilter,
        ('create_date', DateRangeFilter), ('update_date', DateRangeFilter),
    )

    fieldsets = (
        ('INFORMATION', {
            'fields': ("id", "name",  "category", "description", "user", "create_date", "update_date",),
        }),
    )

    inlines = [
        ProductVariantInline,
        ProductImageInline,
        ProductFeatureOptionInline,
        FeatureValueProductInline,
        DraftInline,
    ]

    def initial_approve(modeladmin, request, queryset):
        queryset.update(approved=True)

    def initial_reject(modeladmin, request, queryset):
        queryset.update(approved=False)

    def changed(self, obj):
        return obj.drafts.exists()

    def get_rangefilter_create_date_title(self, request, field_path):
        return 'By create date'

    def get_rangefilter_update_date_title(self, request, field_path):
        return 'By update date'


@admin.register(ProductDraft)
class ProductDraftAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ["id", "original", "category", "name", "description"]
    readonly_fields = list_display
    # actions = ['approve_changes', 'reject_changes']
    search_fields = ['user__email']

    fieldsets = (
        ('INFORMATION', {
            'fields': ("id", "original", "name",  "category", "description"),
        }),
    )

    inlines = [
        ProductDraftFeatureOptionInline,
    ]

    # def approve_changes(modeladmin, request, queryset):
    #     queryset.update(approved=True)
    #
    # def reject_changes(modeladmin, request, queryset):
    #     queryset.update(approved=False)


@admin.register(ProductImage)
class ProductImage(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ("id",   "product", "image",)
    search_fields = ["product__name", "image"]


@admin.register(ProductVariant)
class ProductVariantAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ["id", "product", "name", "description", "inventory", "approved"]
    readonly_fields = list_display + ['current']
    list_filter = ("product__category", "approved")
    search_fields = ['product__user__email', 'product__name', 'product__category__name']

    def get_queryset(self, request):
        qs = super(ProductVariantAdmin, self).get_queryset(request)
        qs = qs.filter(current=True)
        return qs


class FeatureInline(admin.TabularInline):
    model = Feature
    fields = ["id", "name"]
    readonly_fields = fields
    can_delete = False
    show_change_link = False
    extra = 0
    max_num = 0


@admin.register(Category)
class CategoryAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ("id", "name", "parent",)
    list_filter = [MainCategoryListFilter,]
    inlines = [
        CategoryInline,
        ProductInline,
    ]
    search_fields = ['name']


class FeatureOptionInline(admin.TabularInline):
    model = FeatureOption
    fields = ["id", "name"]
    # readonly_fields = fields
    can_delete = True
    show_change_link = True
    extra = 0

    def get_queryset(self, request):
        qs = super(FeatureOptionInline, self).get_queryset(request)
        return qs.order_by('id')


@admin.register(Feature)
class FeatureAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ("id", "name", )
    inlines = [
        FeatureOptionInline,
        FeatureValueInline,
    ]
    search_fields = ['name']


@admin.register(FeatureOption)
class FeatureOptionAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ("id", "feature", "name",)
    search_fields = ['name', 'feature__name']


@admin.register(FeatureValue)
class FeatureValueAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ("id", "feature", "product", "name", )
    search_fields = ['name', 'feature__name', 'product__user__email']
