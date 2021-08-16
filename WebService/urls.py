from django.urls import path
from WebService import views

urlpatterns = [
    path('inicio-sesion/', views.InicioSesion.as_view()),
    path('registrar-paciente/', views.RegistrarPaciente.as_view()),
    path('registrar-familiar/', views.RegistrarFamiliar.as_view()),
]