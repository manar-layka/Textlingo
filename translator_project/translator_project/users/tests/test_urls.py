from django.urls import resolve, reverse

from translator_project.users.models import User


def test_detail(user: User):
    assert reverse("users:user-profile", kwargs={"username": user.username}) == f"api/users/{user.username}/"
    assert resolve(f"api/users/{user.username}/").view_name == "users:user-profile"


def test_update():
    assert reverse("users:update") == "api/users/~update/"
    assert resolve("api/users/~update/").view_name == "users:update"


def test_redirect():
    assert reverse("users:user-redirect") == "api/users/~redirect/"
    assert resolve("api/users/~redirect/").view_name == "users:user-redirect"
