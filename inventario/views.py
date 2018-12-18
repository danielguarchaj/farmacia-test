from rest_framework.views import APIView

from rest_framework import generics
from rest_framework import permissions

from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg, Count, Min, Sum
from rest_framework.response import Response

import datetime


from .models import (
    Proveedor,
    VisitaProveedor,
    Producto,
    Lote,
    Marca,
    PresentacionProducto,
    Categoria,
    Compra,
    Venta,
    Transaccion,
    DetalleVenta
)
from .serializers import (
    ProveedorSerializer,
    ProveedorVisitaSerializer,
    ProductoSerializer,
    ProductoUpdateSerializer,
    ProductoCreateSerializer,
    LoteSerializer,
    LoteDetailedSerializer,
    MarcaSerializer,
    PresentacionSerializer,
    CategoriaSerializer,
    CompraCreateSerializer,
    CompraSerializer,
    CompraDetailSerializer,
    CompraUpdateSerializer,
    VentaCreateSerializer,
    VentaDetailSerializer,
    VentaUpdateSerializer,
    TransaccionesSerializer,
    TransaccionCreateSerializer,

    DetalleVentaSerializer,
    DetalleVentaDetailedLotesSerializer,

    LoteReporteSerializer,

    ProductoSimpleSerializer
)


class ProductosSimpleList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProductoSimpleSerializer
    queryset = Producto.objects.filter(estado=1)


class LotesReporte(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = LoteReporteSerializer
    queryset = Lote.objects.filter(estado=1).order_by('producto')
    

class ReporteTransacciones(generics.ListAPIView):
    serializer_class = TransaccionesSerializer
    def get_queryset(self):        

        fecha_inicio = datetime.date(
            self.kwargs['ys'],
            self.kwargs['ms'],
            self.kwargs['ds']
        )
        fecha_fin = datetime.date(
            self.kwargs['ye'],
            self.kwargs['me'],
            self.kwargs['de']
        )
        queryset = Transaccion.objects.filter(fecha_hora_creacion__range=(
            datetime.datetime.combine(fecha_inicio, datetime.time.min),
            datetime.datetime.combine(fecha_fin, datetime.time.max),
        ),
            estado=1
        )        

        return queryset


class ReporteVentas(generics.ListAPIView):
    serializer_class = VentaDetailSerializer
    def get_queryset(self):        

        fecha_inicio = datetime.date(
            self.kwargs['ys'],
            self.kwargs['ms'],
            self.kwargs['ds']
        )
        fecha_fin = datetime.date(
            self.kwargs['ye'],
            self.kwargs['me'],
            self.kwargs['de']
        )
        queryset = Venta.objects.filter(fecha_hora_creacion__range=(
            datetime.datetime.combine(fecha_inicio, datetime.time.min),
            datetime.datetime.combine(fecha_fin, datetime.time.max),
        ),
            estado=1
        )        

        return queryset



class TotalDebitos(APIView):
    def get(self, request, format=None, **kwargs):
        total = Transaccion.objects.filter(
            estado=1, tipo=1
        ).aggregate(
            total=Sum('monto')
        )
        return Response(total)

class TotalCreditos(APIView):
    def get(self, request, format=None, **kwargs):
        total = Transaccion.objects.filter(
            estado=1, tipo=2
        ).aggregate(
            total=Sum('monto')
        )
        return Response(total)


class LotesUnidadesVendidas(APIView):
    def get(self, request, format=None, **kwargs):
        lote_pk = kwargs.get('lote_pk')
        total = DetalleVenta.objects.filter(
                lote=lote_pk, estado=1
            ).aggregate(
                total=Sum('cantidad')
            )
        return Response(total)


class VentasTotales(APIView):
    def get(self, request, format=None, **kwargs):
        total = Venta.objects.filter(estado=1).aggregate(total=Sum('total'))
        return Response(total)

class ComprasTotales(APIView):
    def get(self, request, format=None, **kwargs):
        total = Compra.objects.filter(estado=1).aggregate(total=Sum('total'))
        return Response(total)


class DetalleVentaList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = DetalleVenta.objects.filter(estado=1).order_by('lote__producto__id')
    serializer_class = DetalleVentaDetailedLotesSerializer


class DetalleVentaRetrieve(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = DetalleVenta.objects.filter(estado=1)
    serializer_class = DetalleVentaDetailedLotesSerializer

class DetalleVentaUpdate(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = DetalleVenta.objects.filter(estado=1)
    serializer_class = DetalleVentaSerializer


class TransaccionCreate(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Transaccion.objects.filter(estado=1)
    serializer_class = TransaccionCreateSerializer

class TransaccionesList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Transaccion.objects.filter(estado=1)
    serializer_class = TransaccionesSerializer

class TransaccionRetrieveUpdate(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Transaccion.objects.filter(estado=1)
    serializer_class = TransaccionesSerializer

class VentaCreate(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Venta.objects.filter(estado=1)
    serializer_class = VentaCreateSerializer



class VentaList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    serializer_class = VentaDetailSerializer
    queryset = Venta.objects.filter(estado=1)
    filter_fields = ('fecha_hora_creacion', )


class VentaRetrieve(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Venta.objects.filter(estado=1)
    serializer_class = VentaDetailSerializer

class VentaUpdate(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Venta.objects.filter(estado=1)
    serializer_class = VentaUpdateSerializer

class LoteDetailList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Lote.objects.filter(estado=1)
    serializer_class = LoteDetailedSerializer

class LoteRetrieveDetail(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Lote.objects.all().exclude(estado=2)
    serializer_class = LoteDetailedSerializer

class LoteRetrieveUpdate(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Lote.objects.all().exclude(estado=2)
    serializer_class = LoteSerializer

class CompraCreate(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Compra.objects.all().exclude(estado=2)
    serializer_class = CompraCreateSerializer


class CompraList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Compra.objects.all().exclude(estado=2)
    serializer_class = CompraSerializer


class CompraRetrieve(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Compra.objects.all().exclude(estado=2)
    serializer_class = CompraDetailSerializer


class CompraUpdate(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Compra.objects.all().exclude(estado=2)
    serializer_class = CompraUpdateSerializer


class ProveedoresListCreate(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Proveedor.objects.all().exclude(estado=2)
    serializer_class = ProveedorSerializer
    

class ProveedoresUpdateRetrieve(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Proveedor.objects.all().exclude(estado=2)
    serializer_class = ProveedorSerializer


class ProveedorVisitaListCreate(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = VisitaProveedor.objects.all()
    serializer_class = ProveedorVisitaSerializer


class ProveedorVisitaUpdateRetrieve(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = VisitaProveedor.objects.all()
    serializer_class = ProveedorVisitaSerializer


class ProductoCreate(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Producto.objects.all().exclude(estado=2)
    serializer_class = ProductoCreateSerializer


class ProductoList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Producto.objects.all().exclude(estado=2)
    serializer_class = ProductoSerializer


class ProductoUpdate(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Producto.objects.all()
    serializer_class = ProductoUpdateSerializer

class ProductoRetrieve(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer


class MarcaListCreate(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Marca.objects.all().exclude(estado=2)
    serializer_class = MarcaSerializer


class MarcaUpdateRetrieve(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer


class PresentacionListCreate(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = PresentacionProducto.objects.all().exclude(estado=2)
    serializer_class = PresentacionSerializer


class PresentacionUpdateRetrieve(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = PresentacionProducto.objects.all()
    serializer_class = PresentacionSerializer


class CategoriaListCreate(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Categoria.objects.all().exclude(estado=2)
    serializer_class = CategoriaSerializer


class CategoriaUpdateRetrieve(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer





# class ProveedorCreate(generics.CreateAPIView):
#     permission_classes = (permissions.IsAuthenticated,)
#     queryset = Consulta.objects.all()
#     serializer_class = ConsultaCreateSerializer

# class ConsultasL(generics.ListAPIView): 
#     permission_classes = (permissions.IsAuthenticated,)
#     queryset = Consulta.objects.all().exclude(estado=2)
#     serializer_class = ConsultaSerializer


# class ConsultaR(generics.RetrieveAPIView):
#     queryset = Consulta.objects.all()
#     serializer_class = ConsultaSerializer

# class ConsultaU(generics.UpdateAPIView):
#     queryset = Consulta.objects.all()
#     serializer_class = ConsultaUpdateSerializer