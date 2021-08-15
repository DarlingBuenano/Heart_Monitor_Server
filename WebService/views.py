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