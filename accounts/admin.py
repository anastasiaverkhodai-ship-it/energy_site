from django.contrib import admin
from .models import Contragent, Agreement

# Реєструємо нові моделі, щоб адмін міг ними керувати
@admin.register(Contragent)
class ContragentAdmin(admin.ModelAdmin):
    list_display = ('name', 'edrpou', 'manager') # поля, які буде видно в списку
    search_fields = ('name', 'edrpou')          # пошук по назві та коду

@admin.register(Agreement)
class AgreementAdmin(admin.ModelAdmin):
    list_display = ('number', 'contragent', 'region', 'date_created')
    list_filter = ('region',)                   # фільтр збоку