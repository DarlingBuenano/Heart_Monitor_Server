from django.urls import path
from WebService import views

urlpatterns = [
    path('inicio-sesion/', views.InicioSesion.as_view()),
    path('regitrarse/', views.Registrarse.as_view()),
]