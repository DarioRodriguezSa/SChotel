# Generated by Django 5.1.1 on 2024-10-05 01:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registrohabitacion',
            name='fecha',
        ),
    ]
