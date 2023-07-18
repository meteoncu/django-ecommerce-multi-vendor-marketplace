from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from app.methods import urlGenerator

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import fields


class StatusAbstract(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = fields.GenericForeignKey('content_type', 'object_id')

    created_at = models.DateTimeField(verbose_name=_('Model Package Field created_at'), null=False, blank=True)

    class Meta:
        abstract = True


class Order(models.Model):
    user = models.ForeignKey('auth.User', verbose_name=_('Model Product Field user'), related_name='orders', on_delete=models.CASCADE)
    created_at = models.DateTimeField(verbose_name=_('Model Field created_at'), null=False, blank=True, editable=False)
    updated_at = models.DateTimeField(verbose_name=_('Model Field updated_at'), null=True, blank=True, editable=False)
    purchased_at = models.DateTimeField(verbose_name=_('Model Order Field purchase_date'), null=True, blank=True, editable=False)

    def save(self, *args, **kwargs):
        if self.created_at is None:
            self.created_at = timezone.now()
        else:
            self.updated_at = timezone.now()
        return super(Order, self).save(*args, **kwargs)


class LineItem(models.Model):
    order = models.ForeignKey(Order, verbose_name=_('Model LineItem Field order'), related_name='lines', on_delete=models.CASCADE)
    product_listing = models.ForeignKey('product.ProductListing', verbose_name=_('Model LineItem Field product_listing'), related_name='lines', on_delete=models.CASCADE)
    count = models.IntegerField(verbose_name=_('Model LineItem Field count'), null=False, blank=False)
    created_at = models.DateTimeField(verbose_name=_('Model LineItem Field create_date'), null=False, blank=True)
    updated_at = models.DateTimeField(verbose_name=_('Model LineItem Field update_date'), null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.created_at is None:
            self.created_at = timezone.now()
        else:
            self.updated_at = timezone.now()
        return super(LineItem, self).save(*args, **kwargs)


class PackageStatus(StatusAbstract):
    CREATED = '0'
    PREPARING = '1'
    PACKAGED = '2'
    IN_CARGO = '3'
    IN_CARGO_TRANSFER = '4'
    IN_CARGO_DISTRIBUTION = '5'
    DELIVERED = '6'
    CANNOT_DELIVERED = '7'

    PACKAGE_STATUSES = [
        ("0", _("Created")),
        ("1", _("Preparing")),
        ("2", _("Packaged")),
        ("3", _("In Cargo")),
        ("4", _("In Cargo Transfer")),
        ("5", _("In Cargo Distribution")),
        ("6", _("Delivered")),
        ("7", _("Cannot delivered")),
    ]

    status = models.CharField(max_length=1, choices=PACKAGE_STATUSES, default='0')


class Package(models.Model):
    order = models.ForeignKey(Order, verbose_name=_('Model Package Field order'), related_name='packages', on_delete=models.CASCADE)
    lines = models.ManyToManyField(LineItem, verbose_name=_('Model Package Field order'), related_name='packages')
    is_shipped = models.BooleanField(verbose_name=_('Model Package Field is_shipped'), null=False, blank=True, default=False)
    is_obsolete = models.BooleanField(verbose_name=_('Model Package Field is_obsolete'), null=False, blank=True, default=False)
    desi = models.FloatField(verbose_name=_('Model Package Field desi'), null=True, blank=True)
    weight = models.FloatField(verbose_name=_('Model Package Field weight'), null=True, blank=True)
    statuses = fields.GenericRelation(PackageStatus)
    created_at = models.DateTimeField(verbose_name=_('Model Package Field create_date'), null=False, blank=True)
    updated_at = models.DateTimeField(verbose_name=_('Model Package Field update_date'), null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.created_at is None:
            self.created_at = timezone.now()
        else:
            self.updated_at = timezone.now()
        return super(Package, self).save(*args, **kwargs)


class ShipmentCompany(models.Model):
    name = models.CharField(verbose_name=_('Model ShipmentCompany Field name'), max_length=100, blank=False, null=False)


class Fulfillment(models.Model):
    package = models.ForeignKey(Order, verbose_name=_('Model Fulfillment Field package'), related_name='fulfillments', on_delete=models.CASCADE)
    shipment_company = models.ForeignKey(ShipmentCompany, verbose_name=_('Model Fulfillment Field shipment_company'), blank=True, null=True, related_name="fulfillments", on_delete=models.SET_NULL)
    tracking_number = models.CharField(verbose_name=_('Model Fulfillment Field tracking_number'), max_length=100, blank=False, null=False)
    tracking_link = models.CharField(verbose_name=_('Model Fulfillment Field tracking_link'), max_length=100, blank=False, null=False)
    is_obsolete = models.BooleanField(verbose_name=_('Model Fulfillment Field is_obsolete'), null=False, blank=True, default=False)
    created_at = models.DateTimeField(verbose_name=_('Model Fulfillment Field create_date'), null=False, blank=True)
    updated_at = models.DateTimeField(verbose_name=_('Model Fulfillment Field update_date'), null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.created_at is None:
            self.created_at = timezone.now()
        else:
            self.updated_at = timezone.now()
        return super(Fulfillment, self).save(*args, **kwargs)
