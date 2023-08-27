# Generated by Django 3.2.8 on 2023-08-25 02:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='inmueble',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('direccion', models.CharField(max_length=250)),
                ('pais', models.CharField(max_length=150)),
                ('descripcion', models.CharField(max_length=500)),
                ('imagen', models.CharField(max_length=900)),
                ('activate', models.BooleanField(default=True)),
            ],
        ),
    ]
