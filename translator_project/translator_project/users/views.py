from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import redirect, render
from django.urls import reverse
from rest_framework import generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from translator.views import TransactionsTemplateHTMLRender

from .serializers import UserProfileSerializer, UserRegistrationSerializer

User = get_user_model()


class UserRegistrationView(generics.CreateAPIView):
    # queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = (permissions.AllowAny,)
    renderer_classes = (TransactionsTemplateHTMLRender,)

    def get(self, request, format=None):
        data = self.serializer_class(self.queryset).data
        return Response(data, template_name="users/user_registration.html")

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            login_url = reverse("users:user-login")
            return redirect(login_url)
        return Response(
            {"message": "Registration failed", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
            template_name="users/user_registration.html",
        )


class UserLoginView(APIView):
    permission_classes = (permissions.AllowAny,)
    renderer_classes = (TransactionsTemplateHTMLRender,)

    def get(self, request, format=None):
        return render(request, "users/user_login.html")

    def post(self, request, format=None):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            token = Token.objects.get(user=user)
            return Response({"token": token.key}, template_name="pages/home.html")
        else:
            return Response({"message": "Invalid Credentials"}, template_name="users/user_login.html")


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = (TransactionsTemplateHTMLRender,)
    lookup_field = "username"
    lookup_url_kwarg = "username"

    def get_queryset(self):
        return User.objects.filter(user=self.request.user)

    def get_object(self):
        return self.request.user

    def get(self, request, username, format=None):
        user = get_object_or_404(User, username=username)
        serializer = self.serializer_class(user)
        return Response(serializer.data, template_name="users/user_details.html")


class UserUpdateView(generics.UpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = (TransactionsTemplateHTMLRender,)
    lookup_field = "username"
    lookup_url_kwarg = "username"

    def get_queryset(self):
        return User.objects.filter(user__username=self.request.user.username)

    def get(self, request, username, format=None):
        user = get_object_or_404(User, username=username)
        serializer = self.serializer_class(user)
        return Response(serializer.data, template_name="users/update_user.html")

    def post(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response_data = {"message": "User information updated successfully"}
            response_data.update(serializer.data)
            return Response(response_data, template_name="users/user_details.html")
        response_data = {"message": "User information not updated due to these errors:"}
        response_data.update(serializer.data)
        return Response(response_data, template_name="users/user_details.html", status=status.HTTP_400_BAD_REQUEST)


class UserRedirectView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        return Response({"redirect_url": reverse("users:user-profile", kwargs={"username": request.user.username})})


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
