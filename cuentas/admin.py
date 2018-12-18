from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User
from .forms import UserChangeForm, UserCreationForm

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = (
        'id',
        'username',
        'nombres',
        'apellidos',
        'is_staff',
        'is_superuser'
    )

    list_filter = ('is_superuser',)

    fieldsets = (
        (None, {'fields': ('username', 'password', 'nombres', 'apellidos')}),
        ('Informacion Personal', {
            'fields': (     
                        'fecha_nacimiento',
                        'direccion',
                        'correo',
                        'foto',
                        'dpi',
                        'telefono',
                        'genero'
                    )
        }),
        ('Permissions', {
            'fields': (
                        'groups',
                        'user_permissions',
                        'is_active',
                        'is_superuser',
                        'is_staff',
                        'tipo'
                    )
        }),
    )

    add_fieldsets = (
        (None, 
            {
                'classes': ('wide',),
                'fields': ('username', 'correo', 'nombres', 'apellidos', 'password1', 'password2')
            }
        ),
    )

    search_fields = ('username', 'nombres', 'apellidos')
    ordering = ('username',)
    filter_horizontal = ()