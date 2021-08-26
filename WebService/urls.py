from django.urls import path
from WebService import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("inicio-sesion/", views.InicioSesion.as_view()),
    path("paciente/", views.Paciente.as_view()),
    path("familiar/", views.Familiar.as_view()),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
