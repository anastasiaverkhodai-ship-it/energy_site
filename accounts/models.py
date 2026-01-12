import os
import uuid
from django.utils.text import slugify
from django.db import models
from django.contrib.auth.models import User

class Contragent(models.Model):
    """Модель контрагента, прив'язана до користувача"""
    name = models.CharField("Назва", max_length=255)
    edrpou = models.CharField("ЄДРПОУ", max_length=10, unique=True)
    manager = models.CharField("Менеджер", max_length=100)
    
    user = models.OneToOneField(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='contragent',
        verbose_name="Користувач (Клієнт)"
    )

    def __str__(self):
        return self.name

class Agreement(models.Model):
    """Модель договору"""
    number = models.CharField("Номер договору", max_length=50)
    contragent = models.ForeignKey(
        Contragent, 
        on_delete=models.CASCADE, 
        related_name='agreements', 
        verbose_name="Контрагент"
    )
    region = models.CharField("Область/Регіон", max_length=100, default="Не вказано")
    date = models.DateField("Дата підписання", null=True, blank=True)
    file = models.FileField("Файл договору", upload_to='agreements/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Договір №{self.number}"

# Функція має бути ПОЗА класом Document, над ним
def upload_to_path(instance, filename):
    # Отримуємо розширення (напр. .pdf або .jpg)
    ext = filename.split('.')[-1]
    # Генеруємо унікальне ім'я за допомогою UUID
    new_filename = f"{uuid.uuid4().hex}.{ext}"
    # Повертаємо шлях: documents/назва_файлу
    return os.path.join('documents/', new_filename)

# ДОДАЄМО КЛАС DOCUMENT, ЯКОГО НЕ ВИСТАЧАЛО
class Document(models.Model):
    DOCUMENT_TYPES = [
        ('Договір', 'Договір'),
        ('Акт', 'Акт'),
        ('Рахунок', 'Рахунок'),
        ('Динаміка обсягів споживання', 'Динаміка обсягів споживання'),
        ('Додаткова угода', 'Додаткова угода'),
        ('Перелік ЕІС-кодів', 'Перелік ЕІС-кодів'),
        ('Повідомлення', 'Повідомлення'),
        ('Інше', 'Інше'),
    ]

    title = models.CharField("Назва файлу", max_length=255)
    document_type = models.CharField(
        "Тип документа",
        max_length=100, 
        choices=DOCUMENT_TYPES, 
        default='Інше'
    )
    contragent = models.ForeignKey(
        Contragent, 
        on_delete=models.CASCADE, 
        related_name='documents', 
        verbose_name="Контрагент",
        null=True, 
        blank=True
    )
    file = models.FileField("Файл", upload_to='documents/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.document_type})"

# ТАКОЖ ДОДАЄМО TARIFFDOCUMENT (якщо він був потрібен раніше)
class TariffDocument(models.Model):
    year = models.IntegerField("Рік")
    name = models.CharField("Назва тарифу", max_length=255)
    file = models.FileField("Файл тарифу", upload_to='tariffs/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.year})"
    
