from django.db import models

class Paciente(models.Model):
    nombres = models.CharField(max_length=75)
    apellidos = models.CharField(max_length=75)
    fecha_nacimiento = models.DateField("Fecha de Nacimiento", auto_now=False, blank=True, null=True)
    lugar_origen = models.CharField("Lugar de origen", max_length=150, blank=True, null=True)
    telefono = models.CharField("Numero de telefono", max_length=20, blank=True, null=True)
    estado = models.PositiveSmallIntegerField(
        choices=[
            (0, 'Inactivo'),
            (1, 'Activo'),
            (2, 'Eliminado')
        ],
        default=1
    )

    def __str__(self):
        return f'{self.nombres} {self.apellidos}'


class Consulta(models.Model):
    presion_arterial = models.CharField(max_length=10, blank=True, null=True)
    latidos_minuto = models.SmallIntegerField("Latidos por Minuto", blank=True, null=True)
    temperatura = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    nivel_azucar = models.DecimalField("Nivel de Azucar", max_digits=8, decimal_places=2, blank=True, null=True)
    peso = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    fecha = models.DateField(auto_now_add=True)
    costo = models.DecimalField(max_digits=8, decimal_places=2)
    paciente = models.ForeignKey(
        Paciente,
        on_delete = models.CASCADE,
        verbose_name  = "Paciente",
        related_name = 'paciente'
    )
    diagnostico_enfermedades = models.CharField(max_length=500, blank=True, null=True)
    diagnostico_anotaciones = models.CharField(max_length=500, blank=True, null=True)
    tratamiento_medicamentos = models.CharField(max_length=500, blank=True, null=True)
    tratamiento_anotaciones = models.CharField(max_length=500, blank=True, null=True)
    estado = models.PositiveSmallIntegerField(
        choices=[
            (0, 'Inactivo'),
            (1, 'Activo'),
            (2, 'Eliminado')
        ],
        default=1
    )

    def __str__(self):
        return self.paciente.nombres +' '+ self.paciente.apellidos + ' ' + str(self.fecha) + ' ' + str(self.costo)
    