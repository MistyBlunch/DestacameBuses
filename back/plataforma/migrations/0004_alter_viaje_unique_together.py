# Generated by Django 4.0.1 on 2022-01-23 13:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plataforma', '0003_viaje_created'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='viaje',
            unique_together={('pasajero', 'created')},
        ),
    ]
