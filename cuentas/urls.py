from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from . import views


app_name = 'cuentas'
urlpatterns = [
    path('user/current/', views.CurrentUser.as_view(), name='current'),
    path('users/', views.UserList.as_view(), name='list'),
    # path('user/create/', views.UserCreate.as_view(), name='create'),
    path('user/<int:pk>/', views.UserDetail.as_view(), name='detail'),
]


urlpatterns = format_suffix_patterns(urlpatterns)