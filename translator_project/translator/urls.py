from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework import routers

from .views import TranslationCreateAPI

router = routers.DefaultRouter()
router.register(r"translator", TranslationCreateAPI)
app_name = "translator"
urlpatterns = [
    path("", include(router.urls)),
    path("translate/", TemplateView.as_view(template_name="translator/translation.html"), name="translation"),
    path("translat-post/", TranslationCreateAPI.as_view({"post": "create"}), name="translation-post"),
]
