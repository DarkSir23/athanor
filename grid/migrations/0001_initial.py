# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-08-18 21:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('objects', '0005_auto_20150403_2339'),
    ]

    operations = [
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(db_index=True, max_length=255, unique=True)),
                ('lock_storage', models.TextField(blank=True, verbose_name='locks')),
                ('setting_ic', models.BooleanField(default=True)),
                ('order', models.SmallIntegerField(default=100)),
                ('description', models.TextField(blank=True, default='This District has no Description!')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ObjectSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quota_cost', models.PositiveIntegerField(default=0)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_objects', to='objects.ObjectDB')),
                ('district', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rooms', to='grid.District')),
                ('object', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='object_settings', to='objects.ObjectDB')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='owned_objects', to='objects.ObjectDB')),
            ],
        ),
    ]
