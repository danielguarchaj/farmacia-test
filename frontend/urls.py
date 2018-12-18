from django.urls import path

from . import views


app_name = 'frontend'

urlpatterns = [
    path('', views.IndexView, name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('consultas/', views.ConsultasView.as_view(), name='consultas'),
    path('consulta_nueva/', views.ConsultaNuevaView.as_view(), name='consulta_nueva'),
    path('consultas/<int:pk>/', views.ConsultaVerView.as_view(), name='consulta_ver'),

    path('pacientes/', views.PacientesView.as_view(), name='pacientes'),

    path('proveedores/', views.ProveedoresView.as_view(), name='proveedores'),
    path('proveedores/<int:pk>/', views.ProveedorVerView.as_view(), name='proveedor_ver'),

    path('productos/', views.ProductosView.as_view(), name='productos'),
    path('productos/<int:pk>/', views.ProductoVerView.as_view(), name='productos_ver'),

    path('ventas/crear/', views.VentaNuevaView.as_view(), name='venta_crear'),
    path('ventas/<int:pk>/', views.VentaVerView.as_view(), name='venta_ver'),

    path('compras/', views.ComprasView.as_view(), name='compras'),
    path('compras/<int:pk>/', views.CompraVerView.as_view(), name='compra_ver'),
    path('compras/crear/', views.CompraNuevaVerView.as_view(), name='compra_nueva'),

    path('categorias/', views.CategoriasView.as_view(), name='categorias'),
    path('marcas/', views.MarcasView.as_view(), name='marcas'),
    path('presentaciones/', views.PresentacionesView.as_view(), name='presentaciones'),

    path('caja/', views.CajaView.as_view(), name='caja'),

    # path('reportes/venta-dia/', views.VentaDelDiaView.as_view(), name='venta_del_dia'),
    # path('reportes/balance-general/', views.BalanceGeneralView.as_view(), name='balance_general'),
    path('reportes/ventas/', views.ReporteVentasView.as_view(), name='reporte_ventas'),
    path('reportes/transacciones/', views.ReporteTransaccionesView.as_view(), name='reporte_transacciones'),
    path('reportes/productos/', views.ReporteProductosView.as_view(), name='reporte_productos'),

]

