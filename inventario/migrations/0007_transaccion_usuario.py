# Generated by Django 2.1 on 2018-11-30 23:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inventario', '0006_auto_20181130_2151'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaccion',
            name='usuario',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='transacciones', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]