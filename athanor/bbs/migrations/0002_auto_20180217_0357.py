# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-17 03:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bbs', '0001_initial'),
        ('objects', '0009_remove_objectdb_db_player'),
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
