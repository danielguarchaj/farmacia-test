from django.urls import path, re_path

from rest_framework.urlpatterns import format_suffix_patterns

from . import views


app_name = 'inventario'
urlpatterns = [
    path('proveedores/', views.ProveedoresListCreate.as_view(), name='proveedores'),
    path('proveedores/<int:pk>/', views.ProveedoresUpdateRetrieve.as_view(), name='proveedoresUptadeRetrieve'),

    path('visitas/', views.ProveedorVisitaListCreate.as_view(), name='proveedor-visitas'),
    path('visitas/<int:pk>/', views.ProveedorVisitaUpdateRetrieve.as_view(), name='proveedor-visita-UpdataRetrieve'),

    path('productos/', views.ProductoList.as_view(), name='productos'),
    path('productos-simple/', views.ProductosSimpleList.as_view(), name='productos-simple'),
    path('productos/create/', views.ProductoCreate.as_view(), name='producto-create'),
    path('productos/<int:pk>/', views.ProductoRetrieve.as_view(), name='producto-retrieve'),
    path('productos/update/<int:pk>/', views.ProductoUpdate.as_view(), name='producto-update-retrieve'),

    path('presentaciones/', views.PresentacionListCreate.as_view(), name='presentaciones'),
    path('presentaciones/<int:pk>/', views.PresentacionUpdateRetrieve.as_view(), name='presentaciones-update-retrieve'),
    
    path('marcas/', views.MarcaListCreate.as_view(), name='marcas'),
    path('marcas/<int:pk>/', views.MarcaUpdateRetrieve.as_view(), name='marcas-update-retrieve'),

    path('categorias/', views.CategoriaListCreate.as_view(), name='categorias'),
    path('categorias/<int:pk>/', views.CategoriaUpdateRetrieve.as_view(), name='categorias-update-retrieve'),

    path('compras/', views.CompraList.as_view(), name='compras'),
    path('compras/create/', views.CompraCreate.as_view(), name='compra-create'),
    path('compras/<int:pk>/', views.CompraRetrieve.as_view(), name='compra-retrieve'),
    path('compras/update/<int:pk>/', views.CompraUpdate.as_view(), name='compra-update'),
    path('compras/totales/', views.ComprasTotales.as_view(), name='compras-totales'),

    path('ventas/', views.VentaList.as_view(), name='venta-list'),
    path('ventas/create/', views.VentaCreate.as_view(), name='venta-create'),
    path('ventas/<int:pk>/', views.VentaRetrieve.as_view(), name='venta-retrieve'),
    path('ventas/update/<int:pk>/', views.VentaUpdate.as_view(), name='venta-update'),
    path('ventas/totales/', views.VentasTotales.as_view(), name='ventas-totales'),

    path('lotes/', views.LoteDetailList.as_view(), name='lotes'),
    path('lotes/<int:pk>/', views.LoteRetrieveUpdate.as_view(), name='lotes-retrieve-update'),
    path('lotes-detailed/<int:pk>/', views.LoteRetrieveDetail.as_view(), name='lotes-retrieve'),
    path('lotes/ventas/<int:lote_pk>/', views.LotesUnidadesVendidas.as_view(), name='lotes-ventas'),

    path('transacciones/', views.TransaccionesList.as_view(), name='transacciones'),
    path('transacciones/<int:pk>/', views.TransaccionRetrieveUpdate.as_view(), name='transaccion-retrieve-update'),
    path('transacciones/create/', views.TransaccionCreate.as_view(), name='transaccion-create'),
    path('transacciones/debitos-totales/', views.TotalDebitos.as_view(), name='transaccion-debitos-totales'),
    path('transacciones/creditos-totales/', views.TotalCreditos.as_view(), name='transaccion-creditos-totales'),


    path('detalles-venta/', views.DetalleVentaList.as_view(), name='detalles-venta'),
    path('detalles-venta/<int:pk>/', views.DetalleVentaRetrieve.as_view(), name='detalles-venta-retrieve'),
    path('detalles-venta/update/<int:pk>/', views.DetalleVentaUpdate.as_view(), name='detalles-venta-update'),

    path('reportes/ventas/<int:ys>/<int:ms>/<int:ds>/<int:ye>/<int:me>/<int:de>/'
            , views.ReporteVentas.as_view(), name='reporte-ventas'),
    path('reportes/transacciones/<int:ys>/<int:ms>/<int:ds>/<int:ye>/<int:me>/<int:de>/'
            , views.ReporteTransacciones.as_view(), name='reporte-ventas'),     
    path('reportes/lotes/', views.LotesReporte.as_view(), name='reporte-lotes'),

]

urlpatterns = format_suffix_patterns(urlpatterns)