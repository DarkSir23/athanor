# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-12 11:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('objects', '0005_auto_20150403_2339'),
        ('communications', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CharacterCustom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.SmallIntegerField(db_index=True, default=0)),
            ],
        ),
        migrations.CreateModel(
            name='CharacterInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='CharacterPool',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.SmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='CharacterPower',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.SmallIntegerField(db_index=True, default=0)),
                ('is_control', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='CharacterStat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.SmallIntegerField(db_index=True, default=0)),
                ('is_favored', models.BooleanField(default=False)),
                ('is_asset', models.BooleanField(default=False)),
                ('is_caste', models.BooleanField(default=False)),
                ('is_supernal', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='CharacterTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('character', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='storyteller', to='objects.ObjectDB')),
            ],
        ),
        migrations.CreateModel(
            name='CustomKind',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(db_index=True, max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='CustomStat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(db_index=True, max_length=40)),
                ('kind', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='custom_stats', to='storyteller.CustomKind')),
            ],
        ),
        migrations.CreateModel(
            name='Exp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(db_index=True, default=0.0)),
                ('reason', models.CharField(max_length=200)),
                ('date_awarded', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='ExpKind',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(db_index=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ExpLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('character', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exp_kinds', to='storyteller.CharacterTemplate')),
                ('kind', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exp_links', to='storyteller.ExpKind')),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(db_index=True, max_length=20)),
                ('ready', models.BooleanField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(db_index=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='InfoKind',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(db_index=True, max_length=40)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='infos', to='storyteller.Game')),
            ],
        ),
        migrations.CreateModel(
            name='MeritCharacter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=120)),
                ('context', models.CharField(max_length=120)),
                ('rating', models.SmallIntegerField(default=0)),
                ('description', models.TextField(blank=True)),
                ('notes', models.TextField(blank=True)),
                ('character', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='merits', to='storyteller.CharacterTemplate')),
            ],
        ),
        migrations.CreateModel(
            name='MeritKind',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(db_index=True, max_length=30)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='merits', to='storyteller.Game')),
            ],
        ),
        migrations.CreateModel(
            name='Pool',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(db_index=True, max_length=70)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pools', to='storyteller.Game')),
            ],
        ),
        migrations.CreateModel(
            name='PoolCommits',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(max_length=150)),
                ('amount', models.SmallIntegerField(default=0)),
                ('pool', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commitments', to='storyteller.CharacterPool')),
            ],
        ),
        migrations.CreateModel(
            name='Power',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(db_index=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='PowerCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(db_index=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='PowerKind',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(db_index=True, max_length=30)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='powers', to='storyteller.Game')),
            ],
        ),
        migrations.CreateModel(
            name='Specialty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(db_index=True, max_length=40)),
                ('rating', models.SmallIntegerField(default=0)),
                ('custom', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='specialties', to='storyteller.CharacterCustom')),
                ('stat', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='specialties', to='storyteller.CharacterStat')),
            ],
        ),
        migrations.CreateModel(
            name='Stat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(db_index=True, max_length=40)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stats', to='storyteller.Game')),
            ],
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(db_index=True, max_length=40)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='templates', to='storyteller.Game')),
            ],
        ),
        migrations.AddField(
            model_name='powercategory',
            name='kind',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='storyteller.PowerKind'),
        ),
        migrations.AddField(
            model_name='power',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='powers', to='storyteller.PowerCategory'),
        ),
        migrations.AddField(
            model_name='meritcharacter',
            name='kind',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='characters', to='storyteller.MeritKind'),
        ),
        migrations.AddField(
            model_name='info',
            name='kind',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='values', to='storyteller.InfoKind'),
        ),
        migrations.AddField(
            model_name='expkind',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='experiences', to='storyteller.Game'),
        ),
        migrations.AddField(
            model_name='exp',
            name='link',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entries', to='storyteller.ExpLink'),
        ),
        migrations.AddField(
            model_name='exp',
            name='source',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='communications.ObjectStub'),
        ),
        migrations.AddField(
            model_name='customkind',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='custom_stats', to='storyteller.Game'),
        ),
        migrations.AddField(
            model_name='charactertemplate',
            name='template',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='characters', to='storyteller.Template'),
        ),
        migrations.AddField(
            model_name='characterstat',
            name='character',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stats', to='storyteller.CharacterTemplate'),
        ),
        migrations.AddField(
            model_name='characterstat',
            name='stat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='characters', to='storyteller.Stat'),
        ),
        migrations.AddField(
            model_name='characterpower',
            name='character',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='powers', to='storyteller.CharacterTemplate'),
        ),
        migrations.AddField(
            model_name='characterpower',
            name='power',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='characters', to='storyteller.Power'),
        ),
        migrations.AddField(
            model_name='characterpool',
            name='character',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pools', to='storyteller.CharacterTemplate'),
        ),
        migrations.AddField(
            model_name='characterpool',
            name='pool',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pools', to='storyteller.Pool'),
        ),
        migrations.AddField(
            model_name='characterinfo',
            name='character',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='infos', to='storyteller.CharacterTemplate'),
        ),
        migrations.AddField(
            model_name='characterinfo',
            name='info',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='characters', to='storyteller.Info'),
        ),
        migrations.AddField(
            model_name='charactercustom',
            name='character',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customs', to='storyteller.CharacterTemplate'),
        ),
        migrations.AddField(
            model_name='charactercustom',
            name='stat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='characters', to='storyteller.CustomStat'),
        ),
        migrations.AlterUniqueTogether(
            name='template',
            unique_together=set([('key', 'game')]),
        ),
        migrations.AlterUniqueTogether(
            name='stat',
            unique_together=set([('key', 'game')]),
        ),
        migrations.AlterIndexTogether(
            name='stat',
            index_together=set([('key', 'game')]),
        ),
        migrations.AlterUniqueTogether(
            name='specialty',
            unique_together=set([('custom', 'key'), ('stat', 'key')]),
        ),
        migrations.AlterUniqueTogether(
            name='powerkind',
            unique_together=set([('key', 'game')]),
        ),
        migrations.AlterUniqueTogether(
            name='powercategory',
            unique_together=set([('key', 'kind')]),
        ),
        migrations.AlterUniqueTogether(
            name='power',
            unique_together=set([('category', 'key')]),
        ),
        migrations.AlterUniqueTogether(
            name='poolcommits',
            unique_together=set([('pool', 'reason')]),
        ),
        migrations.AlterUniqueTogether(
            name='pool',
            unique_together=set([('game', 'key')]),
        ),
        migrations.AlterUniqueTogether(
            name='meritkind',
            unique_together=set([('key', 'game')]),
        ),
        migrations.AlterUniqueTogether(
            name='meritcharacter',
            unique_together=set([('character', 'key', 'context', 'kind')]),
        ),
        migrations.AlterUniqueTogether(
            name='infokind',
            unique_together=set([('key', 'game')]),
        ),
        migrations.AlterIndexTogether(
            name='infokind',
            index_together=set([('key', 'game')]),
        ),
        migrations.AlterUniqueTogether(
            name='info',
            unique_together=set([('key', 'kind')]),
        ),
        migrations.AlterUniqueTogether(
            name='explink',
            unique_together=set([('kind', 'character')]),
        ),
        migrations.AlterUniqueTogether(
            name='expkind',
            unique_together=set([('game', 'key')]),
        ),
        migrations.AlterUniqueTogether(
            name='customstat',
            unique_together=set([('key', 'kind')]),
        ),
        migrations.AlterUniqueTogether(
            name='customkind',
            unique_together=set([('key', 'game')]),
        ),
        migrations.AlterUniqueTogether(
            name='charactertemplate',
            unique_together=set([('template', 'character')]),
        ),
        migrations.AlterUniqueTogether(
            name='characterstat',
            unique_together=set([('character', 'stat')]),
        ),
        migrations.AlterIndexTogether(
            name='characterstat',
            index_together=set([('character', 'stat')]),
        ),
        migrations.AlterUniqueTogether(
            name='characterpower',
            unique_together=set([('character', 'power')]),
        ),
        migrations.AlterUniqueTogether(
            name='characterpool',
            unique_together=set([('character', 'pool')]),
        ),
        migrations.AlterUniqueTogether(
            name='characterinfo',
            unique_together=set([('character', 'info')]),
        ),
    ]
