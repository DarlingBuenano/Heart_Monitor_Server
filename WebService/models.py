from django.db import models


class Usuarios(models.Model):
    usuario = models.CharField(max_length=25)
    clave = models.CharField(max_length=18)
    tipo_cuenta = models.CharField(max_length=8)
    class Meta:
        db_table = 'usuarios'


class Pacientes(models.Model):
    usuario = models.ForeignKey(Usuarios, on_delete=models.PROTECT, related_name="Pacientes")
    nombre1 = models.CharField(max_length=20)
    nombre2 = models.CharField(max_length=20)
    apellido1 = models.CharField(max_length=20)
    apellido2 = models.CharField(max_length=20)
    fecha_nacimiento = models.DateField()
    ruta_foto = models.ImageField(upload_to="perfil", null=True, blank=False)
    genero = models.CharField(max_length=1)
    correo = models.CharField(max_length=50)
    class Meta:
        db_table = 'pacientes'


class Familiares(models.Model):
    usuario = models.ForeignKey(Usuarios, on_delete=models.PROTECT, related_name="Familiares")
    nombres = models.CharField(max_length=20)
    apellidos = models.CharField(max_length=20)
    ruta_foto = models.ImageField(upload_to="perfil", null=True, blank=False)
    paciente = models.ForeignKey(Pacientes, on_delete=models.PROTECT, related_name="Familiares")
    genero = models.CharField(max_length=1)
    celular = models.CharField(max_length=10)
    class Meta:
        db_table = "familiares"


class SaludCardiaca(models.Model):
    paciente = models.ForeignKey(Pacientes, on_delete=models.PROTECT, related_name="SaludCardiaca")
    fecha = models.DateTimeField()
    class Meta:
        db_table = 'salud_cardiaca'


class BPM(models.Model):
    salud_cardiaca = models.ForeignKey(SaludCardiaca, on_delete=models.PROTECT, related_name="BPM")
    bpm = models.CharField(max_length=3)
    hora = models.DateTimeField()
    class Meta:
        db_table = 'bpm'


class Alertas(models.Model):
    paciente = models.ForeignKey(Pacientes, on_delete=models.PROTECT, related_name="Alertas")
    familiar = models.ForeignKey(Familiares, on_delete=models.PROTECT, related_name="Alertas")
    fecha_hora = models.DateTimeField()
    msj_alerta = models.CharField(max_length=400)
    class Meta:
        db_table = 'alertas'


class SMS(models.Model):
    paciente = models.ForeignKey(Pacientes, on_delete=models.PROTECT, related_name="SMS")
    familiar = models.ForeignKey(Familiares, on_delete=models.PROTECT, related_name="SMS")
    fecha_hora = models.DateTimeField()
    msj_sms = models.CharField(max_length=400)
    class Meta:
        db_table = 'sms'