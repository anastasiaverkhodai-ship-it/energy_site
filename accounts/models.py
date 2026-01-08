from django.db import models
from django.contrib.auth.models import User

class Contragent(models.Model):
    """Модель контрагента, прив'язана до користувача"""
    name = models.CharField("Назва", max_length=255)
    edrpou = models.CharField("ЄДРПОУ", max_length=10, unique=True)
    manager = models.CharField("Менеджер", max_length=100)
    
    # Зв'язок OneToOneField дозволяє закріпити ОДНОГО клієнта за ОДНІЄЮ компанією
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