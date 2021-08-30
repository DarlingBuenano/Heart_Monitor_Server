from django.db import models
from WebService.models import Usuarios

class Sesiones(models.Model):
    usuario = models.OneToOneField(Usuarios, on_delete=models.PROTECT, related_name="usuario")
    channel_name = models.CharField(max_length=100)

    class Meta:
        db_table = "sesiones"