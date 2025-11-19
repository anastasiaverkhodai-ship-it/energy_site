from django.contrib import admin
from django import forms
from pyuploadcare.dj.forms import FileWidget
from .models import Document, TariffDocument


# ----- Document -----

class DocumentAdminForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = "__all__"
        widgets = {
            "file": FileWidget,   # ← використовуємо FileUploaderWidget
        }


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    form = DocumentAdminForm
    list_display = ("title", "file")


# ----- TariffDocument -----

class TariffDocumentAdminForm(forms.ModelForm):
    class Meta:
        model = TariffDocument
        fields = "__all__"
        widgets = {
            "file": FileWidget,   # ← тут теж замінюємо
        }


@admin.register(TariffDocument)
class TariffDocumentAdmin(admin.ModelAdmin):
    form = TariffDocumentAdminForm
    list_display = ("name", "year", "file")
