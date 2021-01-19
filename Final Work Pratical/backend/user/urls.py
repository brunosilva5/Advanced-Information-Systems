from django.conf.urls import include
from django.urls import path

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from simple_email.email_confirmation import urls as email_confirmation_urls


# Import the views
from .views import CreateUserView, GetTokenView, DetailUserView


urlpatterns = [
    # Endpoint for creating a user
    path("create/", CreateUserView.as_view(), name="create_user"),
    # Endpoint for user login (get acess token)
    path("auth/login/", GetTokenView.as_view(), name="login_user"),
    # Endpoint for user logout (refresh access token)
    path("auth/login/refresh/", TokenRefreshView.as_view(), name="login_refresh_user"),
    # Endpoint to confirm account
    path("auth/confirm_account/", include(email_confirmation_urls)),
    # Endpoint for details about a user
    path("me/", DetailUserView.as_view(), name="detail_user"),
]
