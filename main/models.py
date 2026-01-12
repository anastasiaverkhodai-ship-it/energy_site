from django.db import models

class Document(models.Model):
    # Створюємо перелік типів документів
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

    title = models.CharField(max_length=255, verbose_name="Назва файлу")
    
    # Нова графа: Тип документу
    document_type = models.CharField(
        max_length=100, 
        choices=DOCUMENT_TYPES, 
        default='Інше',
        verbose_name="Тип документа"
    )
    
    # Твій стандартний Field для файлу
    file = models.FileField(upload_to='documents/', blank=True, null=True, verbose_name="Файл")

    def __str__(self):
        return f"{self.title} — {self.document_type}"

    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документи"


class TariffDocument(models.Model):
    year = models.IntegerField(verbose_name="Рік")
    name = models.CharField(max_length=255, verbose_name="Назва тарифу")
    
    # Твій стандартний Field для файлу тарифів
    file = models.FileField(upload_to='tariffs/', blank=True, null=True, verbose_name="Файл тарифу")

    def __str__(self):
        return f"{self.name} ({self.year})"

    class Meta:
        verbose_name = "Тарифний документ"
        verbose_name_plural = "Тарифні документи"