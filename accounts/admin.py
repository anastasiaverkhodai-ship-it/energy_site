from django.contrib import admin
from .models import Contragent, Agreement

# Реєструємо нові моделі, щоб адмін міг ними керувати
@admin.register(Contragent)
class ContragentAdmin(admin.ModelAdmin):
    list_display = ('name', 'edrpou', 'manager') # поля, які буде видно в списку
    search_fields = ('name', 'edrpou')          # пошук по назві та коду

@admin.register(Agreement)
class AgreementAdmin(admin.ModelAdmin):
    # Якщо ти перейменувала поле на 'date':
    list_display = ('number', 'contragent', 'region', 'date') 
    
    # АБО просто видали четвертий елемент, щоб не було конфлікту:
    # list_display = ('number', 'contragent', 'region')