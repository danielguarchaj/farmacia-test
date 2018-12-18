from django.contrib import admin

from .models import (
    PresentacionProducto,
    Marca,
    Producto,
    Proveedor,
    VisitaProveedor,
    Compra,
    Venta,
    DetalleVenta,
    Transaccion,
    Lote,
    Categoria
)


@admin.register(PresentacionProducto)
class PresentacionProductoAdmin(admin.ModelAdmin):
    pass


@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    pass

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    pass

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    pass


@admin.register(Lote)
class LoteAdmin(admin.ModelAdmin):
    pass


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    pass


@admin.register(VisitaProveedor)
class VisitaProveedorAdmin(admin.ModelAdmin):
    pass


@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    pass


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    pass


@admin.register(DetalleVenta)
class DetalleVentaAdmin(admin.ModelAdmin):
    pass


@admin.register(Transaccion)
class TransaccionAdmin(admin.ModelAdmin):
    pass