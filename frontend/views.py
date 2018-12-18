from django.shortcuts import redirect
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

def IndexView(request):
    if request.user.is_authenticated:
        return redirect(reverse_lazy('frontend:dashboard'))
    else:
        return redirect(reverse_lazy('frontend:login'))

class LoginView(auth_views.LoginView):
    template_name = 'frontend/cuentas/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse_lazy('frontend:dashboard'))
        return super(LoginView, self).dispatch(request, *args, **kwargs)

class LogoutView(auth_views.LogoutView):
    pass

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'frontend/dashboard.html'

class PacientesView(LoginRequiredMixin, TemplateView):
    template_name = 'frontend/consultas/pacientes.html'

class ConsultaNuevaView(LoginRequiredMixin, TemplateView):
    template_name = 'frontend/consultas/consulta_nueva.html'
    def dispatch(self, request, *args, **kwargs):
        if request.user.tipo!=0:
            return redirect(reverse_lazy('frontend:dashboard'))
        return super(ConsultaNuevaView, self).dispatch(request, *args, **kwargs)

class ConsultasView(LoginRequiredMixin, TemplateView):
    template_name = 'frontend/consultas/consultas.html'

class ConsultaVerView(LoginRequiredMixin, TemplateView):
    template_name = 'frontend/consultas/consulta_ver.html'

class ProveedoresView(LoginRequiredMixin, TemplateView):
    template_name = 'frontend/proveedores/proveedores.html'

class ProveedorVerView(LoginRequiredMixin, TemplateView):
    template_name = 'frontend/proveedores/proveedor_ver.html'

class ProductosView(LoginRequiredMixin, TemplateView):
    template_name = 'frontend/productos/productos.html'

class ProductoVerView(LoginRequiredMixin, TemplateView):
    template_name = 'frontend/productos/producto_ver.html'

class ComprasView(LoginRequiredMixin, TemplateView):
    template_name = 'frontend/transacciones/compras.html'
    def dispatch(self, request, *args, **kwargs):
        if request.user.tipo!=0:
            return redirect(reverse_lazy('frontend:dashboard'))
        return super(ComprasView, self).dispatch(request, *args, **kwargs)

class CompraNuevaVerView(LoginRequiredMixin, TemplateView):
    template_name = 'frontend/transacciones/compra_nueva.html'
    def dispatch(self, request, *args, **kwargs):
        if request.user.tipo!=0:
            return redirect(reverse_lazy('frontend:dashboard'))
        return super(CompraNuevaVerView, self).dispatch(request, *args, **kwargs)
    
class CompraVerView(LoginRequiredMixin, TemplateView):
    template_name = 'frontend/transacciones/compra_ver.html'
    def dispatch(self, request, *args, **kwargs):
        if request.user.tipo!=0:
            return redirect(reverse_lazy('frontend:dashboard'))
        return super(CompraVerView, self).dispatch(request, *args, **kwargs)

class CategoriasView(LoginRequiredMixin, TemplateView):
    template_name = 'frontend/productos/categorias.html'

class MarcasView(LoginRequiredMixin, TemplateView):
    template_name = 'frontend/productos/marcas.html'

class PresentacionesView(LoginRequiredMixin, TemplateView):
    template_name = 'frontend/productos/presentaciones.html'

class VentaNuevaView(LoginRequiredMixin, TemplateView):
    template_name = 'frontend/transacciones/venta_nueva.html'

class VentaDelDiaView(LoginRequiredMixin, TemplateView):
    template_name = 'frontend/reportes/ventas_dia.html'

class VentaVerView(LoginRequiredMixin, TemplateView):
    template_name = 'frontend/transacciones/venta_ver.html'

class CajaView(LoginRequiredMixin, TemplateView):
    template_name = 'frontend/transacciones/caja.html'

class BalanceGeneralView(LoginRequiredMixin, TemplateView):
    template_name = 'frontend/reportes/balance_general.html'

class ReporteVentasView(LoginRequiredMixin, TemplateView):
    template_name = 'frontend/reportes/ventas.html'
    def dispatch(self, request, *args, **kwargs):
        if request.user.tipo!=0:
            return redirect(reverse_lazy('frontend:dashboard'))
        return super(ReporteVentasView, self).dispatch(request, *args, **kwargs)

class ReporteTransaccionesView(LoginRequiredMixin, TemplateView):
    template_name = 'frontend/reportes/transacciones.html'
    def dispatch(self, request, *args, **kwargs):
        if request.user.tipo!=0:
            return redirect(reverse_lazy('frontend:dashboard'))
        return super(ReporteTransaccionesView, self).dispatch(request, *args, **kwargs)

class ReporteProductosView(LoginRequiredMixin, TemplateView):
    template_name = 'frontend/reportes/productos.html'
    def dispatch(self, request, *args, **kwargs):
        if request.user.tipo!=0:
            return redirect(reverse_lazy('frontend:dashboard'))
        return super(ReporteProductosView, self).dispatch(request, *args, **kwargs)