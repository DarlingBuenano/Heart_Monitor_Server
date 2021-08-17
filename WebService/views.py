from rest_framework.views import APIView
from rest_framework.response import Response
from WebService.models import *
import json
from django.core.exceptions import ObjectDoesNotExist

class InicioSesion(APIView):
    def post(self, request, format = None):
        if request.method == 'POST':
            
            user = request.POST['usuario']
            passw = request.POST['clave']
            try:
                unUsuario = Usuarios.objects.get(usuario = user, clave = passw)
                json_data = []

                if(unUsuario.tipo_cuenta == 'Paciente'):
                    unPaciente = Pacientes.objects.get(usuario = unUsuario.id)
                    json_data = {
                        "tipo_cuenta": "Paciente",
                        "nombre1": unPaciente.nombre1,
                        "nombre2": unPaciente.nombre2,
                        "apellido1": unPaciente.apellido1,
                        "apellido2": unPaciente.apellido2,
                        "fecha_nacimiento": unPaciente.fecha_nacimiento,
                        "ruta_foto": str(unPaciente.ruta_foto),
                        "genero": unPaciente.genero,
                        "correo": unPaciente.correo,
                    }
                else:
                    unFamiliar = Familiares.objects.get(usuario = unUsuario.id)
                    json_data = {
                        "tipo_cuenta": "Familiar",
                        "nombres": unPaciente.nombres,
                        "apellidos": unPaciente.apellidos,
                        "ruta_foto": str(unPaciente.ruta_foto),
                        "paciente": unPaciente.paciente,
                        "genero": unPaciente.genero,
                        "celular": unPaciente.celular,
                    }
                
                return Response( json_data )
            except ObjectDoesNotExist:
                return Response( {'response': 'Usuario no existe'} )
        else:
            return Response({'response': 'Método no definido para la clase InicioSesion'})
    
    def get(self, request, format = None):
        if request.method == 'GET':
            return Response({'response': 'Metodo get'})


class RegistrarPaciente(APIView):
    def post(self, request, format = None):
        if request.method == 'POST':

            unUsuario = Usuarios()
            unUsuario.usuario = request.POST['usuario']
            unUsuario.clave = request.POST['clave']
            unUsuario.tipo_cuenta = request.POST['tipo_cuenta']
            unUsuario.save()

            unPaciente = Pacientes()
            unPaciente.usuario = unUsuario
            unPaciente.nombre1 = request.POST['nombre1']
            unPaciente.nombre2 = request.POST['nombre2']
            unPaciente.apellido1 = request.POST['apellido1']
            unPaciente.apellido2 = request.POST['apellido2']
            unPaciente.fecha_nacimiento = request.POST['fecha_nacimiento']
            unPaciente.genero = request.POST['genero']
            unPaciente.correo = request.POST['correo']
            unPaciente.save()

            return Response({'paciente': unPaciente.nombre1 + " " + unPaciente.apellido1, 'id': str(unPaciente.id)})
        else:
            return Response({'response': 'Método no definido para la clase RegistrarPaciente'})


class RegistrarFamiliar(APIView):
    def post(self, request, format = None):
        if request.method == 'POST':
            unUsuario = Usuarios()
            unUsuario.usuario = request.POST['usuario']
            unUsuario.clave = request.POST['clave']
            unUsuario.tipo_cuenta = request.POST['tipo_cuenta']
            unUsuario.save()

            unPaciente = Pacientes.objects.get(pk = request.POST['paciente'])

            unFamiliar = Familiares()
            unFamiliar.usuario = unUsuario
            unFamiliar.nombres = request.POST['nombres']
            unFamiliar.apellidos = request.POST['apellidos']
            unFamiliar.paciente = unPaciente
            unFamiliar.genero = request.POST['genero']
            unFamiliar.celular = request.POST['celular']
            unFamiliar.save()

            return Response({'familiar': unFamiliar.nombres, 'id': str(unFamiliar.id)})
        else:
            return Response({'response': 'Método no definido para la clase RegistrarFamiliar'})