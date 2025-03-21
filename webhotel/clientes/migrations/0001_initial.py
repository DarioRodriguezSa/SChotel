# Generated by Django 5.1.1 on 2024-09-25 05:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='genero',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, unique=True, verbose_name='Nombre')),
            ],
            options={
                'verbose_name': 'genero',
                'verbose_name_plural': 'generos',
                'db_table': 'genero',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, verbose_name='Nombre')),
                ('apellido', models.CharField(max_length=50, verbose_name='Apellido')),
                ('dpi', models.CharField(max_length=50, verbose_name='Dpi')),
                ('telefono', models.CharField(max_length=50, verbose_name='Telefono')),
                ('genero', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clientes.genero')),
            ],
            options={
                'verbose_name': 'cliente',
                'verbose_name_plural': 'clientes',
                'db_table': 'cliente',
                'ordering': ['-id'],
            },
        ),
    ]
