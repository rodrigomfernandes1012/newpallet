# Generated by Django 5.2.1 on 2025-06-18 22:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_controller', '0007_alter_valepallet_criado_por_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='valepallet',
            name='usuario_retorno',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='vales_retorno', to='app_controller.pessoajuridica', verbose_name='Usuario Retorno'),
        ),
    ]
