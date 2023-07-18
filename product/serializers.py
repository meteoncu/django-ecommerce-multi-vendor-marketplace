from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from app.methods import urlGenerator
from .models import *
from user.serializers import UserListSerializer

import json


class ProductDraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDraft
        fields = '__all__'
        depth = 0


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        depth = 0


class ProductSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'url', 'images']
        depth = 0


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'
        depth = 0


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = '__all__'
        depth = 0


class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = '__all__'
        depth = 0


class FeatureOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeatureOption
        fields = '__all__'
        depth = 0


class FeatureOptionListSerializer(serializers.ModelSerializer):
    feature = FeatureSerializer()
    class Meta:
        model = FeatureOption
        fields = ['id', 'name', 'feature']
        depth = 0


class ProductVariantLineItemSerializer(serializers.ModelSerializer):
    product = ProductSimpleSerializer()

    class Meta:
        model = ProductVariant
        fields = ['id', 'name', 'description', 'price', 'product']
        depth = 0


class ProductVariantListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['id', 'name', 'description', 'price']
        depth = 0


class ProductVariantCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['product', 'name', 'description', 'price', 'approved']
        depth = 0


class ProductListSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    variants = serializers.SerializerMethodField()
    feature_options = FeatureOptionListSerializer(many=True)

    def get_images(self, obj):
        # Only approved images can be displayed
        images = obj.images.filter(delete=False)
        return ProductImageSerializer(images, many=True).data

    def get_variants(self, obj):
        # Only current and approved variants can be displayed
        variants = obj.variants.filter(current=True, approved=True)
        return ProductVariantListSerializer(variants, many=True).data

    class Meta:
        model = Product
        fields = ['id', 'user', 'category', 'name', 'description', 'url', 'variants', 'images', 'feature_options']
        depth = 0


class ProductUpdatedListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    variants = serializers.SerializerMethodField()
    feature_options = FeatureOptionListSerializer(many=True)
    original = ProductListSerializer()

    def get_user(self, obj):
        return UserListSerializer(obj.original.user).data

    def get_images(self, obj):
        # After approval, images with delete=False will remain
        images = obj.original.images.filter(delete=False)
        return ProductImageSerializer(images, many=True).data

    def get_variants(self, obj):
        # After approval, variants with approved=None will show up
        variants = obj.original.variants.filter(current=True, approved=None)
        if variants.count() == 0:
            variants = obj.original.variants.filter(current=True, approved=True)
        return ProductVariantListSerializer(variants, many=True).data

    class Meta:
        model = ProductDraft
        fields = ['original', 'name', 'description', 'variants', 'images', 'category', 'user', 'feature_options']
        depth = 0


class ProductBasketSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    # line_items = LineItem

    def get_images(self, obj):
        # Only approved images can be displayed
        images = obj.images.filter(delete=False)
        return ProductImageSerializer(images, many=True).data

    def get_variants(self, obj):
        # Only current and approved variants can be displayed
        variants = obj.variants.filter(current=True, approved=True)
        return ProductVariantListSerializer(variants, many=True).data

    class Meta:
        model = Product
        fields = ['id', 'user', 'category', 'name', 'description', 'url', 'variants', 'images']
        depth = 0


class ProductVariantInventorySerializer(serializers.ModelSerializer):
    product = ProductSimpleSerializer()
    class Meta:
        model = ProductVariant
        fields = ['id', 'name', 'product', 'inventory']
        read_only_fields = ('id', 'name', 'product')
        depth = 0


class ProductDetailedSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    variants = serializers.SerializerMethodField()
    feature_options = FeatureOptionListSerializer(many=True)

    def get_images(self, obj):
        # Only approved images can be displayed
        images = obj.images.filter(delete=False)
        return ProductImageSerializer(images, many=True).data

    def get_variants(self, obj):
        # Only current and approved variants can be displayed
        variants = obj.variants.filter(current=True, approved=True)
        return ProductVariantListSerializer(variants, many=True).data

    class Meta:
        model = Product
        fields = ['id', 'user', 'category', 'name', 'description', 'url', 'variants', 'images', 'feature_options',
                  'approved', 'create_date', 'update_date']
        depth = 0


class ProductSetFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['feature_options']
        depth = 0

    def validate(self, data):
        # Initializing needed variables
        product = self.instance
        cat = product.category
        feature_options = data.get('feature_options', None)

        if feature_options:
            # Adding allowed features of the category of the product
            allowed_features = list(cat.features.all())

            # Finding and adding features of every parent category until it is not allowed
            while cat.parent and not cat.disable_parent_features:
                cat = cat.parent
                allowed_features += list(cat.features.all())

            # Checking if new features are in the allowed features
            features_not_allowed = []
            for feature_option in feature_options:
                if feature_option.feature not in allowed_features:
                    features_not_allowed.append(feature_option.feature)
            if len(features_not_allowed) > 0:
                raise ValidationError({"message": "These features are not allowed:" + str(features_not_allowed)})

        return data

    # def update(self, instance, validated_data):
    #     feature_options = validated_data.pop('feature_options', None)
    #
    #     if feature_options:
    #         # Passing newly given M2M objects into the draft object
    #         for feature_option in feature_options:
    #             # Searching for an option with the same feature with the given option
    #             option_of_same_feature = draft.feature_options.filter(feature=feature_option.feature).first()
    #             if option_of_same_feature:
    #                 # Unbinding that option from the draft
    #                 draft.feature_options.remove(option_of_same_feature)
    #             # Binding the new option to the draft
    #             draft.feature_options.add(feature_option)
    #
    #         return instance


class ProductDraftSetFeatureSerializer(ProductSetFeatureSerializer):
    class Meta:
        model = ProductDraft
        fields = ['feature_options']


class ProductCreateSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
                       child=serializers.FileField(max_length=100000,
                                         allow_empty_file=False,
                                         use_url=False), required=False, write_only=True)
    variants = serializers.ListField(
                       child=serializers.CharField(max_length=500), required=False, write_only=True)
    features = FeatureOptionSerializer(many=True, read_only=True)
    feature_options = serializers.ListField(
                       child=serializers.CharField(max_length=500), required=False, write_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'description', 'images', 'variants', 'features', 'feature_options']
        read_only_fields = ['id']
        depth = 0

    def create(self, validated_data):
        images = validated_data.pop('images', None)
        variants = validated_data.pop('variants', None)
        feature_options = validated_data.pop('feature_options', None)

        product = super(ProductCreateSerializer, self).create(validated_data)

        # Images and variants are approved as default since this is initial create
        # This product does not show up until initial approval

        if images:
            images_data = [{"image": image, "product": product.id, "approved": True} for image in images]
            image_serializer = ProductImageSerializer(many=True, data=images_data, required=False)
            try:
                image_serializer.is_valid(raise_exception=True)
            except Exception as e:
                product.delete()
                raise ValidationError({"message": "Images are not allowed"})

        if variants:
            variants = [json.loads(variant) for variant in variants]
            [variant.update({'product': product.id, 'approved': True}) for variant in variants]
            variants_serializer = ProductVariantCreateSerializer(many=True, data=variants)
            try:
                variants_serializer.is_valid(raise_exception=True)
            except Exception as e:
                product.delete()
                raise ValidationError({"message": "Variants are not proper"})

        if feature_options:
            feature_options_serializer = ProductSetFeatureSerializer(product, data={'feature_options': feature_options})
            try:
                feature_options_serializer.is_valid(raise_exception=True)
            except Exception as e:
                product.delete()
                print(e)
                raise ValidationError({"message": "Feature options are not allowed"})

        # Saving all serializers since there is no validation error
        if images:
            image_serializer.save()
        if variants:
            variants_serializer.save()
        if feature_options:
            feature_options_serializer.save()

        return product

    def validate(self, data):
        request = self.context.get("request", None)
        url = urlGenerator(Product, data.get('name'))
        data.update({'user': request.user, 'url': url})
        return data


class ProductUpdateSerializer(serializers.ModelSerializer):
    new_images = serializers.ListField(
        child=serializers.FileField(max_length=100000,
                                    allow_empty_file=False,
                                    use_url=False), default=[], required=False, write_only=True)
    deleted_images = ProductImageSerializer(many=True, required=False, write_only=True)
    variants = serializers.ListField(
                       child=serializers.CharField(max_length=500), required=False, write_only=True)
    features = FeatureOptionSerializer(many=True, read_only=True)
    feature_options = serializers.ListField(
                       child=serializers.CharField(max_length=500), required=False, write_only=True)

    class Meta:
        model = Product
        fields = ['name', 'category', 'description', 'new_images', 'deleted_images', 'variants', 'features', 'feature_options']
        read_only_fields = ()
        depth = 0

    def validate(self, data):
        new_images = data.pop("new_images", None)
        variants = data.pop("variants", None)
        feature_options = data.pop("feature_options", None)

        draft = ProductDraft.objects.filter(original=self.instance).first()
        if draft:
            draft.delete()
        draft = ProductDraft.objects.create(original=self.instance, **data)

        # draft_update_serializer = ProductDraftSerializer(draft, data=data)
        # draft_update_serializer.is_valid(raise_exception=True)
        # data.update({"draft_update_serializer": draft_update_serializer})

        if new_images:
            images_data = [{"image": image, "product": data.instance.id, "approved": None} for image in new_images]
            new_images_serializer = ProductImageSerializer(many=True, data=images_data, required=False)
            new_images_serializer.is_valid(raise_exception=True)
            data.update({"new_images_serializer": new_images_serializer})

        if variants:
            variants = [json.loads(variant) for variant in variants]
            [variant.update({'product': self.instance.id}) for variant in variants]
            variants_serializer = ProductVariantCreateSerializer(many=True, data=variants)
            variants_serializer.is_valid(raise_exception=True)
            data.update({"variants_serializer": variants_serializer})

        if feature_options:
            feature_options_serializer = ProductDraftSetFeatureSerializer(draft, data={'feature_options': feature_options})
            feature_options_serializer.is_valid(raise_exception=True)
            data.update({"feature_options_serializer": feature_options_serializer})

        return data

    def update(self, instance, validated_data):
        feature_options_serializer = validated_data.pop('feature_options_serializer', None)
        if feature_options_serializer:
            feature_options_serializer.save()

        variants_serializer = validated_data.pop('variants_serializer', None)
        if variants_serializer:
            variants_serializer.save()

        new_images_serializer = validated_data.pop('new_images_serializer', None)
        if new_images_serializer:
            new_images_serializer.save()

        deleted_images = validated_data.pop('deleted_images', None)
        if deleted_images:
            data.instance.images.filter(id__exact=deleted_images).update(delete=True)

        draft_update_serializer = validated_data.pop('draft_update_serializer', None)
        if draft_update_serializer:
            draft_update_serializer.save()

        return instance


class ProductDirectUpdateSerializer(serializers.ModelSerializer):
    new_images = serializers.ListField(
        child=serializers.FileField(max_length=100000,
                                    allow_empty_file=False,
                                    use_url=False), default=[], required=False, write_only=True)
    deleted_images = ProductImageSerializer(many=True, required=False, write_only=True)
    variants = serializers.ListField(
                       child=serializers.CharField(max_length=500), required=False, write_only=True)

    class Meta:
        model = Product
        fields = ['name', 'category', 'description', 'new_images', 'deleted_images', 'variants']
        read_only_fields = ()
        depth = 0

    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super(ProductDirectUpdateSerializer, self).__init__(*args, **kwargs)

    def validate(self, data):
        new_images = data.pop("new_images", None)
        deleted_images = data.pop("deleted_images", None)
        variants = data.pop("variants", None)

        if new_images:
            images_data = [{"image": image, "product": data.instance.id, "approved": True} for image in new_images]
            image_serializer = ProductImageSerializer(many=True, data=images_data, required=False)
            try:
                image_serializer.is_valid(raise_exception=True)
            except Exception as e:
                raise Exception(e)
            image_serializer.save()

        if deleted_images:
            data.instance.images.filter(id__exact=deleted_images).delete()

        if variants:
            variants = [json.loads(variant) for variant in variants]
            [variant.update({'product': self.instance.id, 'approved': True}) for variant in variants]
            variants_serializer = ProductVariantCreateSerializer(many=True, data=variants)
            try:
                variants_serializer.is_valid(raise_exception=True)
            except Exception as e:
                raise Exception(e)

            # Hiding old variants of the product
            self.instance.variants.update(current=False)

            # Creating new variants
            variants_serializer.save()

        return data


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        depth = 0


class CategorySimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'parent']
        depth = 0


class CategorySubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
        depth = 0


class CategoryListSerializer(serializers.ModelSerializer):
    subcategories = CategorySubSerializer(many=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'parent', 'subcategories']
        depth = 0


class CategoryRetrieveSerializer(serializers.ModelSerializer):
    subcategories = CategorySubSerializer(many=True)
    products = serializers.SerializerMethodField()

    def get_products(self, obj):
        # Only approved products will be displayed
        products = obj.products.filter(approved=True)
        return ProductListSerializer(products, many=True).data

    class Meta:
        model = Category
        fields = ['id', 'name', 'parent', 'features', 'subcategories', 'products']
        depth = 0


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        extra_kwargs = {"features": {"required": False}}
        depth = 0
