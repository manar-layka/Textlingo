from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError

from .models import Translation


class TranslationSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            raise ValidationError({"detail": "Authentication required"}, code=status.HTTP_401_UNAUTHORIZED)
        return attrs

    class Meta:
        model = Translation
        fields = ("id", "content_type", "original_text", "translated_text", "created_at")
