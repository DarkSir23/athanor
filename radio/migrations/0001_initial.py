# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2017-02-08 04:20
from __future__ import unicode_literals

import athanor.core.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('objects', '0005_auto_20150403_2339'),
        ('comms', '0010_auto_20161206_1912'),
    ]

    operations = [
        migrations.CreateModel(
            name='RadioFrequency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(db_index=True, max_length=255)),
                ('channel', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='frequency', to='comms.ChannelDB')),
            ],
        ),
        migrations.CreateModel(
            name='RadioSlot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(db_index=True, max_length=255)),
                ('codename', models.CharField(blank=True, max_length=255, null=True)),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('color', models.CharField(default='n', max_length=25, validators=[athanor.core.models.validate_color])),
                ('on', models.BooleanField(default=1)),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='radio_slots', to='comms.ChannelDB')),
                ('character', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='radio', to='objects.ObjectDB')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='radioslot',
            unique_together=set([('key', 'character'), ('codename', 'channel')]),
        ),
    ]
