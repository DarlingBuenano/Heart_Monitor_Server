import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from WebService.models import SaludCardiaca, Pacientes, Usuarios
from AppServer.models import Sesiones


class JWSC_SaludCardiaca(JsonWebsocketConsumer):
    usuario_id = 1
    paciente_id = 1
    familiar_id = 1

    def connect(self):
        print("Conexión establecida (salud cardiaca): " + self.channel_name)
        return super().connect()
    

    def receive_json(self, content, **kwargs):
        self.usuario_id = content["usuario"]
        self.paciente_id = content["paciente"]
        self.familiar_id = content["familiar"]

        unUsuario = Usuarios.objects.get(pk=self.usuario_id)
        Sesiones.objects.create(channel_name=self.channel_name, usuario=unUsuario) #guardar la sesión de ese usuario en la bd

        saludCard = SaludCardiaca()
        saludCard.paciente = Pacientes.objects.get(pk=self.paciente_id)
        saludCard.bpm = content["bpm"]
        saludCard.fecha = content["fecha"]
        saludCard.hora = content["hora"]
        saludCard.save()

        self.canal_mensaje()
        return super().receive_json(content, **kwargs)
    

    def disconnect(self, code):
        print("Conexión desconectada (salud cardiaca)")
        Sesiones.objects.filter(channel_name=self.channel_name).delete()
        return super().disconnect(code)
    

    def canal_mensaje(self):
        print(Sesiones.objects.get(usuario=self.usuario_id).channel_name)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.send)(self.channel_name, { #aqui debe especificar a quien le van a mandar los datos (channel_name)
            "type": "recibir.mensaje",
            "text": "98 BPM",
        })
    

    def recibir_mensaje(self, event):
        self.send(text_data=event["text"])