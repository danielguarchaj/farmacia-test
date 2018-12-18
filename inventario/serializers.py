from rest_framework import serializers
from .models import (
    Proveedor,
    VisitaProveedor,
    Lote,
    Producto,
    Marca,
    PresentacionProducto,
    Categoria,
    Compra,
    Venta,
    DetalleVenta,
    Transaccion
)
from cuentas.models import User
from cuentas.serializers import UserSerializer


class TransaccionesSerializer(serializers.ModelSerializer):
    usuario = UserSerializer()
    class Meta:
        model = Transaccion
        fields = '__all__'


class TransaccionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaccion
        exclude = ('usuario', )

    def create(self, validated_data):
        user =  self.context['request'].user
        user_obj = User.objects.get(pk=user.pk)
        transaccion = Transaccion.objects.create(usuario=user_obj, **validated_data)
        return transaccion


class ProveedorVisitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisitaProveedor
        fields = '__all__'


class ProveedorSerializer(serializers.ModelSerializer):
    visitas = serializers.SerializerMethodField()

    class Meta:
        model = Proveedor
        fields = '__all__'
    
    def get_visitas(self, obj):
        try:
            view = self.context['view']
            pk = int(view.kwargs['pk'])
            visitas = VisitaProveedor.objects.filter(proveedor__id=pk).exclude(estado=2)
        except KeyError:
            visitas = VisitaProveedor.objects.filter(proveedor__id=obj.id).exclude(estado=2)
            
        serializer = ProveedorVisitaSerializer(data=visitas, many=True)
        serializer.is_valid()

        return serializer.data


class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = '__all__'


class PresentacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PresentacionProducto
        fields = '__all__'


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'


class LoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lote
        exclude = ('compra', )

class LoteSerializerCompra(serializers.ModelSerializer):
    class Meta:
        model = Lote
        fields = '__all__'

class ProductoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

class ProductoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

class CompraUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compra
        fields = '__all__'


class CompraSerializer(serializers.ModelSerializer):
    lotes = serializers.SerializerMethodField()
    proveedor = ProveedorSerializer()
    class Meta:
        model = Compra
        fields = '__all__'
    
    def get_lotes(self, obj):
        try:
            view = self.context['view']
            pk = int(view.kwargs['pk'])
            lotes = Lote.objects.filter(compra__id=pk).exclude(estado=2)
        except KeyError:
            lotes = Lote.objects.filter(compra__id=obj.id).exclude(estado=2)
            
        serializer = LoteSerializer(data=lotes, many=True)
        serializer.is_valid()

        return serializer.data


class CompraCreateSerializer(serializers.ModelSerializer):
    lotes = LoteSerializer(many=True)

    class Meta:
        model = Compra
        fields = '__all__'

    def create(self, validated_data):
        lotes = validated_data.pop('lotes')
        compra = Compra.objects.create(**validated_data)
        
        for lote in lotes:
            lote_obj = Lote.objects.create(compra=compra, **lote)
            prod = lote_obj.producto.nombre.upper()
            prov = lote_obj.compra.proveedor.nombre.upper()
            lote_obj.codigo = f'{lote_obj.id}-{prod[0]}{prod[1]}-{prov[0]}{prov[1]}'
            if lote_obj.fecha_vencimiento is not None:
                fecha = str(lote_obj.fecha_vencimiento).split('-')
                lote_obj.codigo = f'{lote_obj.codigo}-{fecha[1]}{fecha[0]}'
            lote_obj.save()

        return compra


class ProductoSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'


class ProductoSerializer(serializers.ModelSerializer):
    lotes = serializers.SerializerMethodField()
    marca = MarcaSerializer()   
    categoria = CategoriaSerializer()
    presentacion = PresentacionSerializer()

    class Meta:
        model = Producto
        fields = '__all__'

    def get_lotes(self, obj):

        try:
            view = self.context['view']
            pk = int(view.kwargs['pk'])
            lotes = Lote.objects.filter(producto__id=pk).exclude(estado=2)
        except KeyError:
            lotes = Lote.objects.filter(producto__id=obj.id).exclude(estado=2)
            
        serializer = LoteSerializerCompra(data=lotes, many=True)
        serializer.is_valid()

        return serializer.data

class ProductoDetailSerializer(serializers.ModelSerializer):
    marca = MarcaSerializer()
    presentacion = PresentacionSerializer()
    categoria = CategoriaSerializer()
    class Meta:
        model = Producto
        fields = '__all__'


class LoteDetailedSerializer(serializers.ModelSerializer):
    producto = ProductoDetailSerializer()
    class Meta:
        model = Lote
        fields = '__all__'


class CompraDetailSerializer(serializers.ModelSerializer):
    proveedor = ProveedorSerializer()
    lotes = serializers.SerializerMethodField()
    class Meta: 
        model = Compra
        fields = '__all__'

    def get_lotes(self, obj):
        try:
            view = self.context['view']
            pk = int(view.kwargs['pk'])
            lotes = Lote.objects.filter(compra__id=pk).exclude(estado=2)
        except KeyError:
            lotes = Lote.objects.filter(compra__id=obj.id).exclude(estado=2)
            
        serializer = LoteDetailedSerializer(data=lotes, many=True)
        serializer.is_valid()

        return serializer.data


class DetalleVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleVenta
        exclude = ('venta', )


class DetalleVentaDetailedLotesSerializer(serializers.ModelSerializer):
    lote = LoteDetailedSerializer()
    class Meta:
        model = DetalleVenta
        exclude = ('venta',)


class VentaUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venta
        fields = '__all__'


class VentaCreateSerializer(serializers.ModelSerializer):
    detalle_venta = DetalleVentaSerializer(many=True)

    class Meta:
        model = Venta
        exclude = ('usuario',)

    def create(self, validated_data):
        detalle_venta = validated_data.pop('detalle_venta')
        user =  self.context['request'].user
        user_obj = User.objects.get(pk=user.pk)
        venta = Venta.objects.create(usuario=user_obj, **validated_data)
        
        for detalle in detalle_venta:
            detalle_obj = DetalleVenta.objects.create(venta=venta, **detalle)

        return venta


class VentaDetailSerializer(serializers.ModelSerializer):
    detalle_venta = serializers.SerializerMethodField()
    usuario = UserSerializer()
    class Meta: 
        model = Venta
        fields = '__all__'

    def get_detalle_venta(self, obj):
        try:
            view = self.context['view']
            pk = int(view.kwargs['pk'])
            detalle_venta = DetalleVenta.objects.filter(venta__id=pk).exclude(estado=2)
        except KeyError:
            detalle_venta = DetalleVenta.objects.filter(venta__id=obj.id).exclude(estado=2)
            
        serializer = DetalleVentaDetailedLotesSerializer(data=detalle_venta, many=True)
        serializer.is_valid()

        return serializer.data


class LoteReporteSerializer(serializers.ModelSerializer):
    producto = ProductoDetailSerializer()
    detalle_venta = serializers.SerializerMethodField()
    class Meta: 
        model = Lote
        fields = '__all__'

    def get_detalle_venta(self, obj):
        try:
            view = self.context['view']
            pk = int(view.kwargs['pk'])
            detalle_venta = DetalleVenta.objects.filter(lote__id=pk).exclude(estado=2)
        except KeyError:
            detalle_venta = DetalleVenta.objects.filter(lote__id=obj.id).exclude(estado=2)
            
        serializer = DetalleVentaSerializer(data=detalle_venta, many=True)
        serializer.is_valid()

        return serializer.data