from django.contrib import admin

from .models import (
    Paciente,
    Consulta
)


@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    pass


@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    pass