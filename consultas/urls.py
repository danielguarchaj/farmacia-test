from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from . import views


app_name = 'consultas'
urlpatterns = [
    path('pacientes/', views.PacienteListCreate.as_view(), name='pacientes-list-create'),
    path('pacientes/<int:pk>/', views.PacienteUpdateRetrieve.as_view(), name='pacientes-update-retrieve'),
    path('consultas/', views.ConsultasL.as_view(), name='consultaL'),
    path('consulta-create/', views.ConsultasC.as_view(), name='consultaC'),
    path('consulta-detail/<int:pk>/', views.ConsultaR.as_view(), name='consultaR'),
    path('consulta-update/<int:pk>/', views.ConsultaU.as_view(), name='consultaU'),

    path('consultas/totales/', views.ConsultasTotales.as_view(), name='consultas-totales'),
]

urlpatterns = format_suffix_patterns(urlpatterns)