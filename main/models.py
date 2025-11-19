from django.db import models
from pyuploadcare.dj.models import FileField   # важливо!

class Document(models.Model):
    title = models.CharField(max_length=255)
    file = FileField(blank=True, null=True)   # Uploadcare зберігає файл у хмарі

    def __str__(self):
        return self.title


class TariffDocument(models.Model):
    year = models.IntegerField()
    name = models.CharField(max_length=255)
    file = FileField(blank=True, null=True)   # також через Uploadcare

    def __str__(self):
        return f"{self.name} ({self.year})"



