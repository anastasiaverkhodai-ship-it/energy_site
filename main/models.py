from django.db import models

class Document(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='docs/')

    def __str__(self):
        return self.title



from django.db import models

class TariffDocument(models.Model):
    year = models.IntegerField()
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='docs/')  # тепер файл лежить у media/docs/

    def __str__(self):
        return f"{self.name} ({self.year})"


