from django.urls import include, path
from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns = [
    path("api-auth/", include("rest_framework.urls")),
    path("translator", include("translator.urls")),
    path("users/", include("translator_project.users.urls", namespace="users")),
    path("api-token-auth/", ObtainAuthToken.as_view(), name="api_token_auth"),
]
