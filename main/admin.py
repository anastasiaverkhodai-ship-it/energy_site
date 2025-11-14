

# Register your models here.
from django.contrib import admin
from .models import TariffDocument

@admin.register(TariffDocument)
class TariffDocumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'file')
