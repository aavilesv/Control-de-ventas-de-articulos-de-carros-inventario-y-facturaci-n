# Generated by Django 2.2.4 on 2020-08-26 09:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('seguridad', '0001_initial'),
        ('inventario', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(default='', max_length=200, verbose_name='Nombre')),
                ('direccion', models.CharField(default='', max_length=200, verbose_name='Dirección')),
                ('telefono', models.CharField(default='', max_length=10, verbose_name='Telefono')),
                ('ced_ruc', models.CharField(default='', max_length=14, verbose_name='Cedula o Ruc')),
                ('email', models.CharField(default='', max_length=200, verbose_name='Email')),
                ('status', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaventa', models.DateTimeField(blank=True, default='', verbose_name='Fecha')),
                ('iva', models.DecimalField(decimal_places=0, default=0, max_digits=19, verbose_name='Iva')),
                ('subtotal', models.DecimalField(decimal_places=0, default=0, max_digits=19, verbose_name='Subtotal')),
                ('total', models.DecimalField(decimal_places=0, default=0, max_digits=19, verbose_name='Total')),
                ('descuento', models.DecimalField(decimal_places=0, default=0, max_digits=19, verbose_name='Descuento')),
                ('userfecha', models.DateTimeField(default='', verbose_name='Fechausuario')),
                ('usermodificardor', models.IntegerField(default=0, verbose_name='Descuento')),
                ('userfechamodificador', models.DateTimeField(default='', verbose_name='Fechamodificada')),
                ('status', models.BooleanField(default=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='venta.Cliente')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='seguridad.Empresa')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Venta',
                'verbose_name_plural': 'Ventas',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='DetalleVenta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField(default=0, verbose_name='Cantidad')),
                ('total', models.DecimalField(decimal_places=0, default=0, max_digits=19, verbose_name='Total')),
                ('preciototal', models.DecimalField(decimal_places=0, default=0, max_digits=19, verbose_name='Precio Total')),
                ('articulo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventario.Articulo')),
                ('venta', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='venta.Venta')),
            ],
            options={
                'verbose_name': 'Detalle de Venta',
                'verbose_name_plural': 'Detalle de Ventas',
                'ordering': ['id'],
            },
        ),
    ]
