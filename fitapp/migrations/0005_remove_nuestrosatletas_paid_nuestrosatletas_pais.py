# Generated by Django 5.0.7 on 2025-05-30 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitapp', '0004_nuestrosatletas_paid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nuestrosatletas',
            name='paid',
        ),
        migrations.AddField(
            model_name='nuestrosatletas',
            name='pais',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Pais'),
        ),
    ]
