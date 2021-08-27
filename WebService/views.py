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
                                        "nombres": paciente.nombres,
                                        "apellidos": paciente.apellidos,
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
                                            "nombres": familiar.paciente.nombres,
                                            "apellidos": familiar.paciente.apellidos,
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


class Paciente(APIView):
    def post(self, request, format=None):
        if request.method == "POST":
            try:
                with transaction.atomic():
                    try:
                        if Usuarios.objects.get(nom_usuario=request.POST["usuario"]):
                            return Response({"response": False, "mensaje": "Usuario ya esta creado, intenta con otro nuevamente"})
                    except:
                        pass
                    usuario = Usuarios()
                    usuario.nom_usuario = request.POST["usuario"]
                    usuario.clave = request.POST["clave"]
                    usuario.tipo_cuenta = "Paciente"

                    usuario.full_clean()
                    usuario.save()

                    paciente = Pacientes()
                    paciente.usuario = usuario
                    paciente.nombres = request.POST["nombres"]
                    paciente.apellidos = request.POST["apellidos"]
                    paciente.fecha_nacimiento = request.POST["fecha_nacimiento"]
                    paciente.genero = request.POST["genero"]
                    paciente.correo = request.POST["correo"]

                    paciente.full_clean()
                    paciente.save()
            except Exception:
                return Response({"response": False, "mensaje": "Un campo se encuentra vació, verifica que todos estén completos"})

            return Response({"response": True, "mensaje": "El paciente fue registrado correctamente"})

    def put(self, request, formate=None):
        if request.method == "PUT":
            try:
                with transaction.atomic():
                    usuario = Usuarios.objects.get(nom_usuario=request.POST["usuario"])
                    usuario.clave = request.POST["clave"]

                    paciente = Pacientes.objects.get(usuario=usuario)
                    paciente.nombres = request.POST["nombres"]
                    paciente.apellidos = request.POST["apellidos"]
                    paciente.fecha_nacimiento = request.POST["fecha_nacimiento"]
                    paciente.genero = request.POST["genero"]
                    paciente.correo = request.POST["correo"]

                    usuario.full_clean()
                    usuario.save()
                    paciente.full_clean()
                    paciente.save()
            except Exception as ex:
                return Response({"response": False, "mensaje": "Hubo un error modificar los datos"})
            return Response({"response": True, "mensaje": "Los datos fueron modificado correctamente"})

    def get(self, request, formate=None):
        if request.method == "GET":
            try:
                usuario = Usuarios.objects.get(nom_usuario=request.GET["username"])
                json_data = {}
                if usuario.tipo_cuenta != "Familiar":
                    return Response(
                        {
                            "response": True,
                            "mensaje": "Paciente encontrado",
                            "paciente": {
                                "nombres": usuario.paciente.nombres,
                                "apellidos": usuario.paciente.apellidos,
                            },
                        }
                    )
                else:
                    return Response({"response": False, "mensaje": "Estas intentando añadir un familiar, en vez de un paciente"})
            except Exception as ex:
                return Response({"response": False, "mensaje": "El usuario que esta ingresando no existe, intentalo nuevamente"})


class Familiar(APIView):
    def post(self, request, format=None):
        if request.method == "POST":
            try:
                with transaction.atomic():
                    try:
                        if Usuarios.objects.get(nom_usuario=request.POST["usuario"]):
                            return Response({"response": False, "mensaje": "Usuario ya esta creado, intenta con otro nuevamente"})
                    except:
                        pass
                    try:
                        user_paciente = Usuarios.objects.get(nom_usuario=request.POST["user_paciente"])
                    except:
                        return Response({"response": False, "mensaje": "El paciente que intenta buscar no existe, intenta nuevamente"})
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
                        return Response({"response": False, "mensaje": "Estas intentando añadir un familiar, en vez de un paciente"})
            except Exception as ex:
                return Response({"response": False, "mensaje": "Un campo se encuentra vació, verifica que todos estén completos"})
            return Response({"response": True, "mensaje": "El familiar fue registrado correctamente"})

    def put(self, request, format=None):
        if request.method == "PUT":
            try:
                with transaction.atomic():
                    usuario = Usuarios.objects.get(nom_usuario=request.POST["usuario"])
                    usuario.clave = request.POST["clave"]

                    familiar = Familiares.objects.get(usuario=usuario)
                    familiar.usuario = usuario
                    familiar.nombres = request.POST["nombres"]
                    familiar.apellidos = request.POST["apellidos"]
                    familiar.genero = request.POST["genero"]
                    familiar.celular = request.POST["celular"]

                    usuario.full_clean()
                    usuario.save()
                    familiar.full_clean()
                    familiar.save()
            except Exception as ex:
                return Response({"response": False, "mensaje": "Hubo un error modificar los datos"})
            return Response({"response": True, "mensaje": "Los datos fueron modificado correctamente"})
