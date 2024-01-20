# En conversion/models.py
from django.db import models

class Imagen(models.Model):
    archivo = models.ImageField(upload_to='imagenes/')
    pdf = models.FileField(upload_to='pdfs/', blank=True, null=True)

