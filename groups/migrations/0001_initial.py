# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-10-04 21:18
from __future__ import unicode_literals

import athanor.core.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('objects', '0005_auto_20150403_2339'),
        ('comms', '0009_auto_20160921_1731'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(db_index=True, max_length=255, unique=True)),
                ('lock_storage', models.TextField(blank=True, verbose_name='locks')),
                ('order', models.IntegerField(default=0)),
                ('tier', models.PositiveSmallIntegerField(default=1)),
                ('abbreviation', models.CharField(max_length=10)),
                ('color', models.CharField(default='n', max_length=20, validators=[athanor.core.models.validate_color])),
                ('description', models.TextField(blank=True)),
                ('ic_enabled', models.BooleanField(default=True)),
                ('ooc_enabled', models.BooleanField(default=True)),
                ('display_type', models.SmallIntegerField(default=0)),
                ('timeout', models.DurationField(null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GroupCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(db_index=True, max_length=255, unique=True)),
                ('order', models.PositiveSmallIntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GroupParticipant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=120, null=True)),
                ('character', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='groups', to='objects.ObjectDB')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participants', to='groups.Group')),
            ],
        ),
        migrations.CreateModel(
            name='GroupPermissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=12, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='GroupRank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.IntegerField(default=0)),
                ('name', models.CharField(max_length=35)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ranks', to='groups.Group')),
                ('permissions', models.ManyToManyField(to='groups.GroupPermissions')),
            ],
        ),
        migrations.AddField(
            model_name='groupparticipant',
            name='permissions',
            field=models.ManyToManyField(to='groups.GroupPermissions'),
        ),
        migrations.AddField(
            model_name='groupparticipant',
            name='rank',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='holders', to='groups.GroupRank'),
        ),
        migrations.AddField(
            model_name='group',
            name='alert_rank',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='groups.GroupRank'),
        ),
        migrations.AddField(
            model_name='group',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='groups', to='groups.GroupCategory'),
        ),
        migrations.AddField(
            model_name='group',
            name='guest_permissions',
            field=models.ManyToManyField(to='groups.GroupPermissions'),
        ),
        migrations.AddField(
            model_name='group',
            name='ic_channel',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='group', to='comms.ChannelDB'),
        ),
        migrations.AddField(
            model_name='group',
            name='invites',
            field=models.ManyToManyField(related_name='group_invites', to='objects.ObjectDB'),
        ),
        migrations.AddField(
            model_name='group',
            name='member_permissions',
            field=models.ManyToManyField(to='groups.GroupPermissions'),
        ),
        migrations.AddField(
            model_name='group',
            name='ooc_channel',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='group', to='comms.ChannelDB'),
        ),
        migrations.AddField(
            model_name='group',
            name='start_rank',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='groups.GroupRank'),
        ),
        migrations.AlterUniqueTogether(
            name='grouprank',
            unique_together=set([('name', 'group'), ('num', 'group')]),
        ),
        migrations.AlterUniqueTogether(
            name='groupparticipant',
            unique_together=set([('character', 'group')]),
        ),
    ]
