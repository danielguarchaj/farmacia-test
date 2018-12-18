from rest_framework import serializers
from .models import (
    Paciente,
    Consulta,
)

class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = '__all__'

class ConsultaSerializer(serializers.ModelSerializer):
    paciente = PacienteSerializer()
    class Meta:
        model = Consulta
        fields = '__all__'

class ConsultaCreateSerializer(serializers.ModelSerializer):
    paciente = serializers.PrimaryKeyRelatedField(many=False, queryset=Paciente.objects.all())
    class Meta:
        model = Consulta
        fields = '__all__'


class ConsultaUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consulta
        fields = '__all__'


# class ConsultaCreateSerializer(serializers.ModelSerializer):
#     diagnostico = DiagnosticoCreateSerializer(required=False)
#     paciente = serializers.PrimaryKeyRelatedField(many=False, queryset=Paciente.objects.all())

#     class Meta:
#         model = Consulta
#         fields = '__all__'

#     def create(self, validated_data):        
#         consulta = 0
#         try:
#             diagnostico = validated_data.pop('diagnostico')
#             consulta = Consulta.objects.create(**validated_data)
#             try:
#                 tratamiento = diagnostico.pop('tratamiento')
#                 diagnosticoObj = Diagnostico.objects.create(consulta=consulta, **diagnostico)
#                 Tratamiento.objects.create(diagnostico=diagnosticoObj, **tratamiento)
#             except ValueError:
#                 Diagnostico.objects.create(consulta=consulta, **diagnostico)
#         except ValueError:
#             consulta = Consulta.objects.create(**validated_data)
#         return consulta