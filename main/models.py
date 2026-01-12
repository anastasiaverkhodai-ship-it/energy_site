from django.db import models

class Document(models.Model):
    title = models.CharField(max_length=255)
    # Замінюємо FileField на стандартний Django Field
    file = models.FileField(upload_to='documents/', blank=True, null=True)

    def __str__(self):
        return self.title


class TariffDocument(models.Model):
    year = models.IntegerField()
    name = models.CharField(max_length=255)
    # Замінюємо FileField на стандартний Django Field
    file = models.FileField(upload_to='tariffs/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.year})"