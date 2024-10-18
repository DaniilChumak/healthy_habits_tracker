from django.contrib.auth.views import (LogoutView, PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetView)
from django.urls import path, reverse_lazy
from rest_framework_simplejwt.views import TokenRefreshView

from users.apps import UsersConfig
from users.views import (MyTokenObtainPairView, UserCreateAPIView,
                         UserDestroyAPIView, UserListAPIView,
                         UserUpdateAPIView, recover_password,
                         verification_view)

app_name = UsersConfig.name

urlpatterns = [
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path("register/confirm/<str:token>/", verification_view,
         name="verification"),
    path("<int:pk>/profile/", UserUpdateAPIView.as_view(), name="profile"),
    path("<int:pk>/delete/", UserDestroyAPIView.as_view(), name="delete"),
    path("recover/", recover_password, name="recover"),
    path(
        "password_reset/",
        PasswordResetView.as_view(
            template_name="users/password_reset_form.html",
            email_template_name="users/password_reset_email.html",
            success_url=reverse_lazy("users:login"),
        ),
        name="password_reset",
    ),
    path(
        "password_reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html",
            success_url=reverse_lazy("users:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "password_reset/complete/",
        PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path("", UserListAPIView.as_view(), name="users"),
    path("login/", MyTokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
