from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

from .models import Boleto


@staff_member_required
def filtros(request, *args, **kwargs):
    return render(request, "boletos/filtros.html")
