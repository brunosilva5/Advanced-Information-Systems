from .views import verify
from django.urls import path


urlpatterns = [
    path("verify/<str:hashed_user_id>/<str:token>", verify, name="verify_email_token")
]
