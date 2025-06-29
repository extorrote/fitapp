# Generated by Django 5.0.7 on 2025-06-10 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitapp', '0028_alter_comprasuplementofarmaco_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comprasuplementofarmaco',
            options={},
        ),
        migrations.AddField(
            model_name='comprasuplementofarmaco',
            name='ciudad',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='comprasuplementofarmaco',
            name='codigo_postal',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='comprasuplementofarmaco',
            name='direccion_texto',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='comprasuplementofarmaco',
            name='envio_realizado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='comprasuplementofarmaco',
            name='estado',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='comprasuplementofarmaco',
            name='nombre_completo',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='comprasuplementofarmaco',
            name='pais',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='comprasuplementofarmaco',
            name='telefono',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
