from django.urls import path
from WebService import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('inicio-sesion/', views.InicioSesion.as_view()),
    path('registrar-paciente/', views.RegistrarPaciente.as_view()),
    path('registrar-familiar/', views.RegistrarFamiliar.as_view()),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)