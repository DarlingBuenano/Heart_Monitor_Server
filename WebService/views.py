from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from WebService.models import *
import json


class InicioSesion(APIView):
    def post(self, request, format=None):
        if request.method == "POST":
            try:
                user = request.POST["usuario"]
                passw = request.POST["clave"]
                if not user == passw == "" and not user == "":
                    try:
                        usuario = Usuarios.objects.get(nom_usuario=user)
                        json_data = {}
                        if usuario.clave == passw:
                            if usuario.tipo_cuenta == "Paciente":
                                paciente = Pacientes.objects.get(usuario=usuario.id)
                                json_familiar = []
                                for familiar in paciente.familiares.all():
                                    json_familiar.append(
                                        {
                                            "id": familiar.id,
                                            "nombres": familiar.nombres,
                                            "apellidos": familiar.apellidos,
                                            "ruta_foto": str(familiar.ruta_foto),
                                            "genero": familiar.genero,
                                            "celular": familiar.celular,
                                        }
                                    )
                                json_data = {
                                    "response": True,
                                    "mensaje": "El usuario esta logeado",
                                    "usuario": user,
                                    "paciente": {
                                        "tipo_cuenta": "Paciente",
                                        "id": paciente.id,
                                        "fir_nombre": paciente.nombre1,
                                        "sec_nombre": paciente.nombre2,
                                        "fir_apellido": paciente.apellido1,
                                        "sec_apellido": paciente.apellido2,
                                        "fecha_nacimiento": paciente.fecha_nacimiento,
                                        "ruta_foto": str(paciente.ruta_foto),
                                        "genero": paciente.genero,
                                        "correo": paciente.correo,
                                        "familiares": json_familiar,
                                    },
                                }
                            else:
                                familiar = Familiares.objects.get(usuario=usuario.id)
                                json_data = {
                                    "response": True,
                                    "mensaje": "El usuario esta logeado",
                                    "usuario": user,
                                    "familiar": {
                                        "tipo_cuenta": "Familiar",
                                        "id": familiar.id,
                                        "nombres": familiar.nombres,
                                        "apellidos": familiar.apellidos,
                                        "ruta_foto": str(familiar.ruta_foto),
                                        "genero": familiar.genero,
                                        "celular": familiar.celular,
                                        "paciente": {
                                            "usuario": familiar.paciente.usuario.nom_usuario,
                                            "id": familiar.paciente.id,
                                            "fir_nombre": familiar.paciente.nombre1,
                                            "sec_nombre": familiar.paciente.nombre2,
                                            "fir_apellido": familiar.paciente.apellido1,
                                            "sec_apellido": familiar.paciente.apellido2,
                                            "fecha_nacimiento": familiar.paciente.fecha_nacimiento,
                                            "ruta_foto": str(familiar.paciente.ruta_foto),
                                            "genero": familiar.paciente.genero,
                                            "correo": familiar.paciente.correo,
                                        },
                                    },
                                }
                        else:
                            json_data = {
                                "response": False,
                                "mensaje": "Contraseña incorrecta, intentelo nuevamente",
                            }
                        return Response(json_data)
                    except ObjectDoesNotExist:
                        return Response({"response": False, "mensaje": "El usuario no existe, registrate o intentalo de nuevo"})
                else:
                    return Response({"response": False, "mensaje": "Campos vacios, ingrese un usuario y contraseña"})
            except:
                return Response({"response": False, "mensaje": "Faltan los parametros"})
        else:
            return Response({"response": False, "mensaje": "Método GET no definido"})


class RegistrarPaciente(APIView):
    def post(self, request, format=None):
        if request.method == "POST":
            try:
                with transaction.atomic():
                    usuario = Usuarios()
                    usuario.nom_usuario = request.POST["usuario"]
                    usuario.clave = request.POST["clave"]
                    usuario.tipo_cuenta = "Paciente"

                    usuario.full_clean()
                    usuario.save()

                    paciente = Pacientes()
                    paciente.usuario = usuario
                    paciente.nombre1 = request.POST["nombre1"]
                    paciente.nombre2 = request.POST["nombre2"]
                    paciente.apellido1 = request.POST["apellido1"]
                    paciente.apellido2 = request.POST["apellido2"]
                    paciente.fecha_nacimiento = request.POST["fecha_nacimiento"]
                    paciente.genero = request.POST["genero"]
                    paciente.correo = request.POST["correo"]

                    paciente.full_clean()
                    paciente.save()
            except Exception:
                return Response({"response": False, "mensaje": "Ups! hubo un error al registrar el paciente, intentelo nuevamente "})

            return Response({"response": True, "mensaje": "El paciente fue registrado correctamente"})
        else:
            return Response({"response": False, "mensaje": "Método Get no definido"})


class RegistrarFamiliar(APIView):
    def post(self, request, format=None):
        if request.method == "POST":
            try:
                with transaction.atomic():
                    user_paciente = Usuarios.objects.get(nom_usuario=request.POST["paciente"])
                    if user_paciente.tipo_cuenta == "Paciente":
                        usuario = Usuarios()
                        usuario.nom_usuario = request.POST["usuario"]
                        usuario.clave = request.POST["clave"]
                        usuario.tipo_cuenta = "Familiar"

                        usuario.full_clean()
                        usuario.save()

                        familiar = Familiares()
                        familiar.usuario = usuario
                        familiar.nombres = request.POST["nombres"]
                        familiar.apellidos = request.POST["apellidos"]
                        familiar.paciente = user_paciente.paciente
                        familiar.genero = request.POST["genero"]
                        familiar.celular = request.POST["celular"]

                        familiar.full_clean()
                        familiar.save()
                    else:
                        return Response({"response": False, "mensaje": "Ups! esta enlazando el Familiar con otro Familiar"})
            except Exception as ex:
                return Response({"response": False, "mensaje": "Ups! hubo un error al registrar al familiar, intentelo nuevamente"})

            return Response({"response": True, "mensaje": "El familiar fue registrado correctamente"})
        else:
            return Response({"response": False, "mensaje": "Método Get no definido"})
