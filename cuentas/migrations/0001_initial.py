# Generated by Django 2.1 on 2018-11-25 01:01

import cuentas.managers
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=150, unique=True, verbose_name='username')),
                ('correo', models.EmailField(max_length=254, unique=True, verbose_name='correo electronico')),
                ('nombres', models.CharField(max_length=50, verbose_name='nombres')),
                ('apellidos', models.CharField(max_length=50, verbose_name='apellidos')),
                ('fecha_nacimiento', models.DateField(blank=True, null=True, verbose_name='fecha de nacimiento')),
                ('direccion', models.CharField(blank=True, max_length=150, null=True, verbose_name='direccion')),
                ('foto', models.ImageField(blank=True, null=True, upload_to='media/cuentas/fotos')),
                ('dpi', models.CharField(blank=True, max_length=15, null=True, verbose_name='DPI')),
                ('telefono', models.CharField(blank=True, max_length=15, null=True, verbose_name='Numero de telefono')),
                ('genero', models.PositiveSmallIntegerField(choices=[(0, 'Sin Definir'), (1, 'Hombre'), (2, 'Mujer')], default=0, verbose_name='genero')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='is_superuser')),
                ('is_staff', models.BooleanField(default=False, verbose_name='is_staff')),
                ('estado', models.PositiveSmallIntegerField(choices=[(0, 'Inactivo'), (1, 'Activo'), (2, 'Eliminado')], default=1)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', cuentas.managers.UserManager()),
            ],
        ),
    ]
