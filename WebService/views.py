from rest_framework.views import APIView
from rest_framework.response import Response
from WebService.models import *
import json

class InicioSesion(APIView):
    def post(self, request, format = None):
        if request.method == 'POST':
            return Response({'response': 'POST de Inicio de sesión en mantenimiento'})
        return Response({'response': 'Clase Inicio de sesión en mantenimiento'})
    
    def get(self, request, format = None):
        if request.method == 'GET':
            return Response({'response': 'Este mensaje es de prueba. Este método GET será eliminado'})


class Registrarse(APIView):
    def post(self, request, format = None):
        if request.method == 'POST':
            return Response({'response': 'POST de Registrarse en mantenimiento'})
        return Response({'response': 'Clase Registrarse en mantenimiento'})

"""
try:
    json_data = json.loads(request.body.decode('utf-8'))
    cedula = json_data['cedula']
    nombres = (json_data['nombres']).split()
    nombre1 = nombres[0]
    nombre2 = nombres[1]
    apellido1 = nombres[2]
    apellido2 = nombres[3]
    unCiudadano = ciudadanos.objects.get(cedula=cedula, nombre1__icontains=nombre1, nombre2__icontains=nombre2, apellido1__icontains=apellido1, apellido2__icontains=apellido2)
    json_consulta = {
        "nombres": json_data['nombres'].upper(),
        "provincia": unCiudadano.provincia.provincia,
        "canton": unCiudadano.canton.canton,
        "centro_vacunacion": unCiudadano.centroVacunacion.centro_vacunacion,
        "direccion": unCiudadano.centroVacunacion.direccion,
        "primera_dosis": unCiudadano.primeraDosis,
        "segunda_dosis": unCiudadano.segundaDosis
    }
    return Response({"consulta": json_consulta})    
except ciudadanos.DoesNotExist:
    return Response({"mensaje": "Ups, no se encuentra registrado...."})
"""