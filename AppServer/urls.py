from django.urls import path
from AppServer import views

urlpatterns = [
    path('index/', views.vwIndex)
]