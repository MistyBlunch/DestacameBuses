# Generated by Django 4.0.1 on 2022-01-21 22:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('plataforma', '0002_alter_bus_placa'),
    ]

    operations = [
        migrations.AddField(
            model_name='viaje',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
