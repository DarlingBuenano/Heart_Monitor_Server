from django.urls import path
from AppServer.jsonConsumer import JWSC_SaludCardiaca

ws_urlpatterns = [
    path('wsocket/guardarSalurCardiaca/', JWSC_SaludCardiaca.as_asgi())
]