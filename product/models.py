from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from app.methods import urlGenerator


class Feature(models.Model):
    name = models.CharField(verbose_name=_('Model Feature Field name'), max_length=100, blank=False, null=False)

    def __str__(self):
        return self.name


class FeatureOption(models.Model):
    feature = models.ForeignKey(Feature, verbose_name=_('Model FeatureOption Field feature'), related_name='options', on_delete=models.CASCADE)
    name = models.CharField(verbose_name=_('Model FeatureOption Field name'), max_length=100, blank=False, null=False)

    def __str__(self):
        return self.name


class Category(models.Model):
    parent = models.ForeignKey('self', verbose_name=_('Model Category Field parent'), related_name='subcategories', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(verbose_name=_('Model Category Field name'), max_length=100, blank=False, null=False)
    features = models.ManyToManyField(Feature, verbose_name=_('Model Category Field features'), blank=True)
    disable_parent_features = models.BooleanField(verbose_name=_('Model Category Field disable_parent_features'), default=False)

    def __str__(self):
        return self.name


class Product(models.Model):
    user = models.ForeignKey('auth.User', verbose_name=_('Model Product Field user'), related_name='products', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, verbose_name=_('Model Product Field category'), related_name='products', null=False, blank=True, on_delete=models.CASCADE)
    name = models.CharField(verbose_name=_('Model Product Field title'), max_length=100, blank=False, null=False)
    description = models.CharField(verbose_name=_('Model Product Field description'), max_length=100, blank=False, null=False)
    url = models.CharField(verbose_name=_('Model Product Field url'), max_length=100, unique=True, editable=False)
    approved = models.BooleanField(verbose_name=_('Model Product Field approved'), default=None, blank=True, null=True)
    create_date = models.DateTimeField(verbose_name=_('Model Field create_date'), null=False, blank=True, editable=False)
    update_date = models.DateTimeField(verbose_name=_('Model Field update_date'), null=True, blank=True, editable=False)
    feature_options = models.ManyToManyField(FeatureOption, verbose_name=_('Model Product Field feature_options'))

    def __init__(self, *args, **kwargs):
        super(Product, self).__init__(*args, **kwargs)
        self.__name = self.name

    def save(self, *args, **kwargs):
        if self.create_date is None:
            self.create_date = timezone.now()
        else:
            self.update_date = timezone.now()

        if self.__name != self.name:
            self.url = urlGenerator(Product, self.name)

        return super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductDraft(models.Model):
    original = models.ForeignKey(Product, verbose_name=_('Model ProductDraft Field original'), related_name='drafts', null=False, blank=True, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, verbose_name=_('Model ProductDraft Field category'), related_name='drafts', null=False, blank=True, on_delete=models.CASCADE)
    name = models.CharField(verbose_name=_('Model ProductDraft Field title'), max_length=100, blank=False, null=False)
    description = models.CharField(verbose_name=_('Model ProductDraft Field description'), max_length=100, blank=False, null=False)
    feature_options = models.ManyToManyField(FeatureOption, verbose_name=_('Model ProductDraft Field feature_options'))


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, verbose_name=_('Model ProductImage Field product'), related_name='variants', on_delete=models.CASCADE)
    name = models.CharField(verbose_name=_('Model ProductVariant Field name'), max_length=100, blank=True, null=False)
    description = models.CharField(verbose_name=_('Model ProductVariant Field description'), max_length=100, blank=True, null=False)
    feature_options = models.ManyToManyField(FeatureOption, verbose_name=_('Model ProductVariant Field feature_options'))
    inventory = models.PositiveIntegerField(verbose_name=_('Model ProductVariant Field inventory'), blank=True, null=False, default=0)
    current = models.BooleanField(verbose_name=_('Model ProductVariant Field current'), default=True)
    approved = models.BooleanField(verbose_name=_('Model ProductVariant Field approved'), default=None, blank=True, null=True)
    create_date = models.DateTimeField(verbose_name=_('Model Field create_date'), null=False, blank=True, editable=False)
    update_date = models.DateTimeField(verbose_name=_('Model Field update_date'), null=True, blank=True, editable=False)

    def save(self, *args, **kwargs):
        if self.create_date is None:
            self.create_date = timezone.now()
        else:
            self.update_date = timezone.now()

        return super(ProductVariant, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductVariantDraft(models.Model):
    original = models.ForeignKey(ProductVariant, verbose_name=_('Model ProductVariantDraft Field original'), related_name='drafts', null=False, blank=True, on_delete=models.CASCADE)
    name = models.CharField(verbose_name=_('Model ProductDraft Field title'), max_length=100, blank=False, null=False)
    description = models.CharField(verbose_name=_('Model ProductDraft Field description'), max_length=100, blank=False, null=False)
    feature_options = models.ManyToManyField(FeatureOption, verbose_name=_('Model ProductDraft Field feature_options'))


class ProductListing(models.Model):
    product_variant = models.ForeignKey(Product, verbose_name=_('Model ProductListing Field product_variant'), related_name='listings', on_delete=models.CASCADE)
    price = models.FloatField(verbose_name=_('Model ProductListing Field price'), blank=True, null=False)
    is_obsolete = models.BooleanField(verbose_name=_('Model ProductListing Field is_obsolete'), null=False, blank=True, default=False)
    create_date = models.DateTimeField(verbose_name=_('Model ProductListing create_date'), null=False, blank=True, editable=False)

    def save(self, *args, **kwargs):
        if self.create_date is None:
            self.create_date = timezone.now()

        return super(ProductListing, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, verbose_name=_('Model ProductImage Field product'), related_name='images', on_delete=models.CASCADE)
    image = models.FileField(upload_to="images", verbose_name=_('Model ProductImage Field image'), blank=False, null=False)
    approved = models.BooleanField(verbose_name=_('Model ProductImage Field approved'), default=None, blank=True, null=True)
    delete = models.BooleanField(verbose_name=_('Model ProductImage Field delete'), default=False, blank=True, null=True)

    def __str__(self):
        return self.image


class FeatureValue(models.Model):
    feature = models.ForeignKey(Feature, verbose_name=_('Model FeatureValue Field feature'), related_name='values', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name=_('Model FeatureValue Field product'), related_name='feature_values', on_delete=models.CASCADE)
    name = models.CharField(verbose_name=_('Model FeatureValue Field name'), max_length=100, blank=False, null=False)

    def __str__(self):
        return self.name
