from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('username'), max_length=150, unique=True)
    correo = models.EmailField(_('correo electronico'), unique=True)
    nombres = models.CharField(_('nombres'), max_length=50)
    apellidos = models.CharField(_('apellidos'), max_length=50)
    fecha_nacimiento = models.DateField(
        _('fecha de nacimiento'), 
        auto_now=False,
        blank=True, 
        null=True
    )
    direccion = models.CharField(
        _('direccion'),
        max_length=150,
        blank=True, 
        null=True
    )
    foto = models.ImageField(
        upload_to='media/cuentas/fotos',
        blank=True, 
        null=True
    )
    dpi = models.CharField(
        _('DPI'),
        max_length=15,
        blank=True, 
        null=True
    )
    telefono = models.CharField(
        _('Numero de telefono'),
        max_length=15,
        blank=True, 
        null=True
    )
    genero = models.PositiveSmallIntegerField(
        _('genero'),
        choices = [
            (0, 'Sin Definir'),
            (1, 'Hombre'),
            (2, 'Mujer')
        ],
        default=0
    )
    date_joined = models.DateTimeField(
        _('date joined'),
        auto_now_add=True
    )
    tipo = models.PositiveSmallIntegerField(
        _('tipo de usuario'),
        choices = [
            (0, 'admin'),
            (1, 'vendedor')
        ],
        default=0
    )
    is_active = models.BooleanField(
        _('active'),
        default = True
    )
    is_superuser = models.BooleanField(
        _('is_superuser'),
        default=False
    )
    is_staff = models.BooleanField(
        _('is_staff'),
        default=False
    )
    estado = models.PositiveSmallIntegerField(
        choices=[
            (0, 'Inactivo'),
            (1, 'Activo'),
            (2, 'Eliminado')
        ],
        default=1
    )

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['correo', 'nombres', 'apellidos']

    def get_full_namae(self):
        full_name = f'{self.nombres} {self.apellidos}'
        return full_name.strip()
    
    def get_short_name(self):
        return self.nombres