from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User

from .serializers import *
from .permissions import *


class UserViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        if self.action == 'list':
            queryset = User.objects.all()
        else:
            queryset = User.objects.all()
        return queryset

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'list':
            return UserListSerializer
        elif self.action == 'update':
            return UserUpdateSerializer
        elif self.action == "create":
            return UserCreateSerializer
        else:
            return UserSerializer

    def get_permissions(self):
        if self.action == 'create' or self.action == 'login':
            permission_classes = [AllowAny]
        elif self.action == 'retrieve' or self.action == 'update':
            permission_classes = [IsSelf]
        else:
            # List, Destroy
            permission_classes = [IsAdmin]
        return [permission() for permission in permission_classes]

    def get_serializer_context(self):
        context = super(UserViewSet, self).get_serializer_context()
        context.update({"request": self.request})
        return context

    @action(detail=False, methods=['POST'], name='login')
    def login(self, request, *args, **kwargs):
        data = request.data
        email = data.get('email')
        password = data.get('password')

        user = User.objects.filter(email=email).first()
        if not user:
            raise ValidationError({"message": "There is no such a user"})
        if not user or not user.check_password(password):
            raise ValidationError({"message": "Wrong password"})

        try:
            token = Token.objects.get(user=user)
        except Token.DoesNotExist:
            token = Token.objects.create(user=user)

        response_data = UserSerializer(user).data
        response_data.update({'token': str(token)})
        response_data.pop('password')
        response_data.pop('user_permissions')
        response_data.pop('groups')

        return Response(response_data, status=200)
