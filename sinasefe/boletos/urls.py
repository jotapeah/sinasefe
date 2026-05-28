from django.urls import path

from . import views

app_name = "boletos"

urlpatterns = [
    path("", views.filtros, name="filtros"),
]
