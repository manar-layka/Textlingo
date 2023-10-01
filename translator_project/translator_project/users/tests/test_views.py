from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from ..serializers import UserRegistrationSerializer

User = get_user_model()


class UserRegistrationViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse("users:user-registration")

    def test_user_registration(self):
        user_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword",
            "confirm_password": "testpassword",
        }

        serializer = UserRegistrationSerializer(data=user_data)
        serializer.is_valid()
        response = self.client.post(self.register_url, user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        user_exists = User.objects.filter(username="testuser").exists()
        self.assertTrue(user_exists)

    def test_user_registration_failure(self):
        invalid_user_data = {"username": "", "email": "testuser@example.com", "password": "testpassword"}
        response = self.client.post(self.register_url, invalid_user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Registration failed", response.data["message"])
        user_exists = User.objects.filter(username="testuser").exists()
        self.assertFalse(user_exists)


class UserLoginViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse("users:user-login")

        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="testpassword"
        )

    def test_user_login(self):
        login_data = {"username": "testuser", "password": "testpassword"}
        response = self.client.post(self.login_url, login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_user_login_failure(self):
        invalid_login_data = {"username": "testuser", "password": "invalidpassword"}
        response = self.client.post(self.login_url, invalid_login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Invalid Credentials", response.data["message"])


class UserUpdateViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="testpassword"
        )
        self.login_url = reverse("users:user-login")
        self.update_url = reverse("users:update", args=[self.user.username])

    def test_user_update(self):
        login_data = {"username": "testuser", "password": "testpassword"}
        self.client.post(self.login_url, login_data, format="json")
        updated_user_data = {"username": "newusername", "email": "newemail@example.com"}
        response = self.client.post(self.update_url, updated_user_data, format="json")
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_201_CREATED])
        self.assertIn("User information updated successfully", response.data["message"])
        updated_user = User.objects.get(username="newusername")
        self.assertEqual(updated_user.email, "newemail@example.com")

    def test_user_update_failure(self):
        login_data = {"username": "testuser", "password": "testpassword"}
        self.client.post(self.login_url, login_data, format="json")
        invalid_user_data = {"username": "", "email": "newemail@example.com"}
        response = self.client.post(self.update_url, invalid_user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("User information not updated due to these errors:", response.data["message"])
        updated_user = User.objects.get(username="testuser")
        self.assertNotEqual(updated_user.email, "newemail@example.com")
