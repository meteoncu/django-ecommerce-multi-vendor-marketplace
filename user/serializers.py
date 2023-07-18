from .models import *
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ('id',)
        depth = 0


class UserUpdateSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(required=False, write_only=True)
    password = serializers.CharField(required=False, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'password', 'new_password']
        read_only_fields = ('id',)
        depth = 0

        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'password': {'required': False},
            'new_password': {'required': False},
        }

    def validate_password(self, value):
        if value and not self.instance.check_password(value):
            raise ValidationError({"message": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        password = validated_data.get('password')
        new_password = validated_data.get('new_password')

        if first_name:
            instance.first_name = first_name
        if last_name:
            instance.last_name = last_name
        if new_password:
            if not password:
                raise ValidationError({"message": "Old password must be given"})
            instance.set_password(new_password)

        instance.save()
        return instance


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email']
        read_only_fields = ('id',)
        depth = 0


class UserCreateSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'password2']
        read_only_fields = ('id',)
        depth = 0

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        password2 = data.get("password2")

        check_user = User.objects.filter(email=email).first()
        if check_user:
            raise ValidationError({"message": "Email is taken"})
        if password != password2:
            raise ValidationError({"message": "Passwords don't match"})

        return data

    def create(self, validated_data):
        email = validated_data.get('email')
        first_name = validated_data.get('first_name', "")
        last_name = validated_data.get('last_name', "")
        password = validated_data.get('password', "")

        user = User(
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.save()

        return user
