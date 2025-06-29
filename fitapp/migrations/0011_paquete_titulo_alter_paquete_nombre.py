# Generated by Django 5.0.7 on 2025-05-30 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitapp', '0010_delete_contenidopaquete'),
    ]

    operations = [
        migrations.AddField(
            model_name='paquete',
            name='titulo',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='paquete',
            name='nombre',
            field=models.CharField(choices=[('rutina_basica', 'Rutina Básica'), ('dieta_basica', 'Dieta Básica'), ('completo_basico', 'Completo Básico (Dieta + Rutina)'), ('rutina_premium', 'Rutina Premium'), ('dieta_premium', 'Dieta Premium'), ('completo_premium', 'Completo Premium (Dieta + Rutina)')], max_length=50, verbose_name='Categoria de Paquete'),
        ),
    ]
