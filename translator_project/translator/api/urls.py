from django.urls import path

from .views import TranslationView, UserRegistrationView

app_name = "translator"

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="user-registration"),
    path("translate/", TranslationView.as_view(), name="translate-text"),
]
