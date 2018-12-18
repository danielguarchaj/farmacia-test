from rest_framework.views import APIView

from django.db.models import Avg, Count, Min, Sum

from rest_framework.response import Response

from rest_framework import generics
from rest_framework import permissions

from .models import (
    Consulta,
    Paciente
)
from .serializers import (
    ConsultaSerializer,
    ConsultaUpdateSerializer,
    ConsultaCreateSerializer,
    PacienteSerializer
)

class ConsultasTotales(APIView):
    def get(self, request, format=None, **kwargs):
        total = Consulta.objects.filter(estado=1).aggregate(total=Sum('costo'))
        return Response(total)
    

class PacienteListCreate(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Paciente.objects.all().exclude(estado=2)
    serializer_class = PacienteSerializer


class PacienteUpdateRetrieve(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Paciente.objects.all().exclude(estado=2)
    serializer_class = PacienteSerializer


class ConsultasL(generics.ListAPIView): 
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Consulta.objects.all().exclude(estado=2)
    serializer_class = ConsultaSerializer

class ConsultasC(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Consulta.objects.all()
    serializer_class = ConsultaCreateSerializer

class ConsultaR(generics.RetrieveAPIView):
    queryset = Consulta.objects.all()
    serializer_class = ConsultaSerializer

class ConsultaU(generics.UpdateAPIView):
    queryset = Consulta.objects.all()
    serializer_class = ConsultaUpdateSerializer