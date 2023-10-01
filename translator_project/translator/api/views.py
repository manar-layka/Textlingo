import googletrans
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Translation
from .serializers import TranslationSerializer, UserSerializer

# Create your views here.
User = get_user_model()


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)


class TokenGenerationView(APIView):
    def post(self, request, format=None):
        token, created = Token.objects.get_or_create(user=request.user)
        return Response({"token": token.key})


class TranslationView(generics.CreateAPIView):
    queryset = Translation.objects.all()
    serializer_class = TranslationSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        user = self.request.user
        content_type = request.data.get("content_type")
        original_text = request.data.get("original_text")
        translator = googletrans.Translator()
        translated_text = translator.translate(original_text, dest="en").text
        translation = Translation(
            user=user, content_type=content_type, original_text=original_text, translated_text=translated_text
        )
        translation.save()

        return Response({"message": "Translation successful"}, status=status.HTTP_201_CREATED)
