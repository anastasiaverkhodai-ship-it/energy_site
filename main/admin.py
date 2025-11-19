from django.contrib import admin
from .models import Document, TariffDocument


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("title", "file")


@admin.register(TariffDocument)
class TariffDocumentAdmin(admin.ModelAdmin):
    list_display = ("name", "year", "file")
