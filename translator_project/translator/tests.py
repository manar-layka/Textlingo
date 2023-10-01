from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import Translation
from .serializers import TranslationSerializer

User = get_user_model()


class TranslationCreateAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="test_user", email="test_user@example.com", password="test_password"
        )
        self.another_user = User.objects.create_user(
            username="another_test_user", email="another_test_user@example.com", password="test_password"
        )
        self.client.force_authenticate(user=self.user)
        self.create_url = reverse("translator:translation-post")

    def test_create_translation_html(self):
        translation_data = {
            "content_type": "HTML",
            "original_text": "<p>Hallo, wie geht's ?!</p>",
        }

        response = self.client.post(self.create_url, translation_data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("translated_text", response.data)
        self.assertEqual(response.data["translated_text"], "<p>Hello, how are you ?!</p>")
        translation_exists = Translation.objects.filter(user=self.user).exists()
        self.assertTrue(translation_exists)

    def test_create_translation_plain_text(self):
        translation_data = {
            "content_type": "plain text",
            "original_text": "Hallo, wie geht's ?!",
        }
        response = self.client.post(self.create_url, translation_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("translated_text", response.data)
        self.assertEqual(response.data["translated_text"], "Hello, how are you ?!")
        translation_exists = Translation.objects.filter(user=self.user).exists()
        self.assertTrue(translation_exists)

    def test_create_translation_invalid_content_type(self):
        invalid_translation_data = {
            "content_type": "invalid_type",
            "original_text": "Hallo, wie geht's ?!",
        }
        response = self.client.post(self.create_url, invalid_translation_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid content_type", response.data["detail"])
        translation_exists = Translation.objects.filter(user=self.user).exists()
        self.assertFalse(translation_exists)

    def test_list_translations(self):
        translation1 = Translation.objects.create(
            user=self.user, content_type="plain text", original_text="Hello", translated_text="Bonjour"
        )
        translation2 = Translation.objects.create(
            user=self.user, content_type="HTML", original_text="<p>Goodbye</p>", translated_text="<p>Au revoir</p>"
        )
        list_url = reverse("translator:translation-list")
        response = self.client.get(list_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["data"]), 2)

    def test_list_translations_html(self):
        translation = Translation.objects.create(
            user=self.user, content_type="HTML", original_text="<p>Bonjour</p>", translated_text="<p>Hello</p>"
        )
        another_translation = Translation.objects.create(
            user=self.another_user, content_type="HTML", original_text="<p>Hallo</p>", translated_text="<p>Hello</p>"
        )
        list_html_url = reverse("translator:translation-list")
        response = self.client.get(list_html_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["data"]), 1)
        self.assertEqual(response.data["data"][0]["id"], translation.pk)

    def test_list_translations_failure(self):
        self.client.logout()
        list_url = reverse("translator:translation-list")
        response = self.client.get(list_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
