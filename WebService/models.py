from django.db import models
from fernet_fields import EncryptedTextField
from django.core.exceptions import ValidationError


class Usuarios(models.Model):
    nom_usuario = models.CharField(max_length=25, null=False, blank=False, unique=True)
    clave = EncryptedTextField()
    tipo_cuenta = models.CharField(max_length=8)

    class Meta:
        db_table = "usuarios"


class Pacientes(models.Model):
    usuario = models.OneToOneField(Usuarios, on_delete=models.PROTECT, related_name="paciente")
    nombres = models.CharField(max_length=20)
    apellidos = models.CharField(max_length=20)
    fecha_nacimiento = models.DateField()
    ruta_foto = models.ImageField(upload_to="perfil", null=True, blank=True)
    genero = models.CharField(max_length=1)
    correo = models.CharField(max_length=50)

    class Meta:
        db_table = "pacientes"


class Familiares(models.Model):
    usuario = models.OneToOneField(Usuarios, on_delete=models.PROTECT, related_name="familiar")
    nombres = models.CharField(max_length=20)
    apellidos = models.CharField(max_length=20)
    ruta_foto = models.ImageField(upload_to="perfil", null=True, blank=True)
    paciente = models.ForeignKey(Pacientes, on_delete=models.PROTECT, related_name="familiares")
    genero = models.CharField(max_length=1)
    celular = models.CharField(max_length=10)

    class Meta:
        db_table = "familiares"


class SaludCardiaca(models.Model):
    paciente = models.ForeignKey(Pacientes, on_delete=models.PROTECT, related_name="salud_cardiaca")
    bpm = models.CharField(max_length=3, blank=True)
    fecha = models.DateField()
    hora = models.TimeField()

    class Meta:
        db_table = "salud_cardiaca"


class Alertas(models.Model):
    paciente = models.ForeignKey(Pacientes, on_delete=models.PROTECT, related_name="alertas")
    familiar = models.ForeignKey(Familiares, on_delete=models.PROTECT, related_name="alertas")
    fecha_hora = models.DateTimeField()
    msj_alerta = models.CharField(max_length=400)

    class Meta:
        db_table = "alertas"


class SMS(models.Model):
    paciente = models.ForeignKey(Pacientes, on_delete=models.PROTECT, related_name="SMS")
    familiar = models.ForeignKey(Familiares, on_delete=models.PROTECT, related_name="SMS")
    fecha_hora = models.DateTimeField()
    msj_sms = models.CharField(max_length=400)

    class Meta:
        db_table = "sms"
