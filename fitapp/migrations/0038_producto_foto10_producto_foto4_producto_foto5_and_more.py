# Generated by Django 5.0.7 on 2025-06-16 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitapp', '0037_remove_suplementosyfarmacos_laboratorio'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='foto10',
            field=models.ImageField(blank=True, null=True, upload_to='productos/'),
        ),
        migrations.AddField(
            model_name='producto',
            name='foto4',
            field=models.ImageField(blank=True, null=True, upload_to='productos/'),
        ),
        migrations.AddField(
            model_name='producto',
            name='foto5',
            field=models.ImageField(blank=True, null=True, upload_to='productos/'),
        ),
        migrations.AddField(
            model_name='producto',
            name='foto6',
            field=models.ImageField(blank=True, null=True, upload_to='productos/'),
        ),
        migrations.AddField(
            model_name='producto',
            name='foto7',
            field=models.ImageField(blank=True, null=True, upload_to='productos/'),
        ),
        migrations.AddField(
            model_name='producto',
            name='foto8',
            field=models.ImageField(blank=True, null=True, upload_to='productos/'),
        ),
        migrations.AddField(
            model_name='producto',
            name='foto9',
            field=models.ImageField(blank=True, null=True, upload_to='productos/'),
        ),
    ]
