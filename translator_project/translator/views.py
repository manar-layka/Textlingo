# translations/api/views.py
import requests
from bs4 import BeautifulSoup
from googletrans import Translator
from rest_framework import generics, status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response

from .models import Translation
from .serializers import TranslationSerializer


class TransactionsTemplateHTMLRender(TemplateHTMLRenderer):
    def get_template_context(self, data, renderer_context):
        data = super().get_template_context(data, renderer_context)
        if not data:
            return {}
        else:
            return {"data": data}


class TranslationCreateAPI(viewsets.ModelViewSet):
    queryset = Translation.objects.all()
    serializer_class = TranslationSerializer
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes = (
        JSONRenderer,
        TransactionsTemplateHTMLRender,
    )
    template_name = "translator/translation.html"

    def get_queryset(self):
        return Translation.objects.filter(user_id=self.request.user.pk)

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        content_type = request.data.get("content_type")
        original_text = request.data.get("original_text")

        if content_type not in ["HTML", "plain text"]:
            return Response({"detail": "Invalid content_type"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            translator = Translator()

            if content_type == "HTML":
                soup = BeautifulSoup(original_text, "html.parser")

                for element in soup.find_all():
                    if element.string:
                        translated_element = translator.translate(element.string, dest="en")
                        element.string = translated_element.text

                translated_html = str(soup)
                translated_text = translated_html
            else:
                translation_result = translator.translate(original_text, dest="en")
                translated_text = translation_result.text

        except Exception as e:
            translated_text = "Translation error: " + str(e)

        translation = Translation(
            user=request.user,
            content_type=content_type,
            original_text=original_text,
        )

        translation.translated_text = translated_text

        translation.save()

        serializer = self.get_serializer(translation)

        if request.accepted_renderer.format == "html":
            return Response({"data": serializer.data}, template_name=self.template_name)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        if request.accepted_renderer.format == "html":
            return Response({"data": serializer.data}, template_name="translator/translation-list.html")

        return Response({"data": serializer.data})
