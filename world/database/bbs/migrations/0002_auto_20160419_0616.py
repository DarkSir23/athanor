# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-19 06:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('objects', '0005_auto_20150403_2339'),
        ('bbs', '0001_initial'),
        ('groups', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='boardgroup',
            name='group',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='board', to='groups.Group'),
        ),
        migrations.AddField(
            model_name='board',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='boards', to='bbs.BoardGroup'),
        ),
        migrations.AddField(
            model_name='board',
            name='ignore_list',
            field=models.ManyToManyField(to='objects.ObjectDB'),
        ),
        migrations.AlterUniqueTogether(
            name='boardgroup',
            unique_together=set([('group', 'main')]),
        ),
        migrations.AlterUniqueTogether(
            name='board',
            unique_together=set([('category', 'key'), ('category', 'order')]),
        ),
    ]
