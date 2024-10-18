import secrets
import string
from datetime import datetime

import pytz
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from config import settings
from users.models import User
from users.serializers import MyTokenObtainPairSerializer, UserSerializer


# Create your views here.
class UserCreateAPIView(CreateAPIView):
    """Контроллер создания пользователя"""
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class MyTokenObtainPairView(TokenObtainPairView):
    """Контроллер авторизации пользователя"""
    serializer_class = MyTokenObtainPairSerializer

    def perform_authentication(self, request):
        auth_header = request.headers.get("Authorization")
        if auth_header:
            try:
                token = auth_header.split()[1]
                user = User.objects.filter(verification_code=token).first()
                if user:
                    zone = pytz.timezone(settings.TIME_ZONE)
                    user.last_login = datetime.now(zone)
                    user.save()
            except AttributeError as e:
                print(e)


class UserUpdateAPIView(UpdateAPIView):
    """Контроллер редактирования профиля пользователя"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserListAPIView(ListAPIView):
    """Контроллер вывода списка пользователей"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserDestroyAPIView(DestroyAPIView):
    """Контроллер удаления пользователя"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


def verification_view(request, token):
    """Функция верификации пользователя"""
    user = User.objects.filter(verification_code=token).first()
    if user:
        user.is_active = True
        user.save()
    return redirect("users:login")


def recover_password(request):
    """Функция восстановления пароля"""
    alphabet = string.ascii_letters + string.digits
    password = "".join(secrets.choice(alphabet) for i in range(10))
    request.user.set_password(password)
    request.user.save()
    message = f"Ваш новый пароль:\n{password}"
    send_mail(
        "Смена пароля",
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email],
        fail_silently=False,
    )
    return redirect(reverse("catalog:product_list"))