# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-25 21:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('botnet', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bot',
            name='bot',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='botdb', to='scripts.ScriptDB'),
        ),
    ]
