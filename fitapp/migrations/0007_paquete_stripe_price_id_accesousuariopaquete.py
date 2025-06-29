# Generated by Django 5.0.7 on 2025-05-30 19:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitapp', '0006_contenidodieta_contenidorutina_paquete'),
    ]

    operations = [
        migrations.AddField(
            model_name='paquete',
            name='stripe_price_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.CreateModel(
            name='AccesoUsuarioPaquete',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tiene_acceso', models.BooleanField(default=False)),
                ('fecha_pago', models.DateTimeField(blank=True, null=True)),
                ('stripe_payment_id', models.CharField(blank=True, max_length=255, null=True)),
                ('paquete', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fitapp.paquete')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fitapp.registrousuario')),
            ],
        ),
    ]
