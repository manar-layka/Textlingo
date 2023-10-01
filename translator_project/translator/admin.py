from django.contrib import admin

# Register your models here.
from .models import Translation


@admin.register(Translation)
class TranslationAdmin(admin.ModelAdmin):
    pass
