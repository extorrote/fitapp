# Generated by Django 5.0.7 on 2025-06-10 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitapp', '0026_remove_direcciondeenvio_pagado'),
    ]

    operations = [
        migrations.AddField(
            model_name='comprasuplementofarmaco',
            name='tipo_de_producto',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='comprasuplementofarmaco',
            name='titulo_producto',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
