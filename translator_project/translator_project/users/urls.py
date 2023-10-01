from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("register/", views.UserRegistrationView.as_view(), name="user-registration"),
    path("login/", views.UserLoginView.as_view(), name="user-login"),
    path("profile/<str:username>/", views.UserProfileView.as_view(), name="user-profile"),
    path("update/<str:username>/", views.UserUpdateView.as_view(), name="update"),
    path("redirect/", views.UserRedirectView.as_view(), name="user-redirect"),
]
