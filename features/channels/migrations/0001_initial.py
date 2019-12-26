# Generated by Django 2.2.6 on 2019-12-03 00:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        ('actors', '0012_merge_20191110_2125'),
        ('typeclasses', '0013_auto_20191015_1922'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChannelCategoryDB',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('db_key', models.CharField(db_index=True, max_length=255, verbose_name='key')),
                ('db_typeclass_path', models.CharField(db_index=True, help_text="this defines what 'type' of entity this is. This variable holds a Python path to a module with a valid Evennia Typeclass.", max_length=255, null=True, verbose_name='typeclass')),
                ('db_date_created', models.DateTimeField(auto_now_add=True, verbose_name='creation date')),
                ('db_lock_storage', models.TextField(blank=True, help_text="locks limit access to an entity. A lock is defined as a 'lock string' on the form 'type:lockfunctions', defining what functionality is locked and how to determine access. Not defining a lock means no access is granted.", verbose_name='locks')),
                ('db_attributes', models.ManyToManyField(help_text='attributes on this object. An attribute can hold any pickle-able python object (see docs for special cases).', to='typeclasses.Attribute')),
                ('db_channel_typeclass', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='channels', to='core.TypeclassMap')),
                ('db_subscription_typeclass', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='channels', to='core.TypeclassMap')),
                ('db_tags', models.ManyToManyField(help_text='tags on this object. Tags are simple string markers to identify, group and alias actors.', to='typeclasses.Tag')),
            ],
            options={
                'verbose_name': 'ChannelCategory',
                'verbose_name_plural': 'ChannelCategories',
            },
        ),
        migrations.CreateModel(
            name='ChannelDB',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('db_key', models.CharField(db_index=True, max_length=255, verbose_name='key')),
                ('db_typeclass_path', models.CharField(db_index=True, help_text="this defines what 'type' of entity this is. This variable holds a Python path to a module with a valid Evennia Typeclass.", max_length=255, null=True, verbose_name='typeclass')),
                ('db_date_created', models.DateTimeField(auto_now_add=True, verbose_name='creation date')),
                ('db_lock_storage', models.TextField(blank=True, help_text="locks limit access to an entity. A lock is defined as a 'lock string' on the form 'type:lockfunctions', defining what functionality is locked and how to determine access. Not defining a lock means no access is granted.", verbose_name='locks')),
                ('db_keep_log', models.BooleanField(default=False)),
                ('db_attributes', models.ManyToManyField(help_text='attributes on this object. An attribute can hold any pickle-able python object (see docs for special cases).', to='typeclasses.Attribute')),
                ('db_category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='channel_links', to='channels.ChannelCategoryDB')),
                ('db_tags', models.ManyToManyField(help_text='tags on this object. Tags are simple string markers to identify, group and alias actors.', to='typeclasses.Tag')),
            ],
            options={
                'verbose_name': 'Channel',
                'verbose_name_plural': 'Channel',
                'unique_together': {('db_key', 'db_category')},
            },
        ),
        migrations.CreateModel(
            name='SubscriptionDB',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('db_key', models.CharField(db_index=True, max_length=255, verbose_name='key')),
                ('db_typeclass_path', models.CharField(db_index=True, help_text="this defines what 'type' of entity this is. This variable holds a Python path to a module with a valid Evennia Typeclass.", max_length=255, null=True, verbose_name='typeclass')),
                ('db_date_created', models.DateTimeField(auto_now_add=True, verbose_name='creation date')),
                ('db_lock_storage', models.TextField(blank=True, help_text="locks limit access to an entity. A lock is defined as a 'lock string' on the form 'type:lockfunctions', defining what functionality is locked and how to determine access. Not defining a lock means no access is granted.", verbose_name='locks')),
                ('db_voice', models.CharField(blank=True, max_length=255, null=True)),
                ('db_codename', models.CharField(blank=True, max_length=255, null=True)),
                ('db_gagged', models.BooleanField(default=False)),
                ('db_enabled', models.BooleanField(default=True)),
                ('db_attributes', models.ManyToManyField(help_text='attributes on this object. An attribute can hold any pickle-able python object (see docs for special cases).', to='typeclasses.Attribute')),
                ('db_channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to='channels.ChannelDB')),
                ('db_character', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='channel_subs', to='actors.ObjectDB')),
                ('db_tags', models.ManyToManyField(help_text='tags on this object. Tags are simple string markers to identify, group and alias actors.', to='typeclasses.Tag')),
            ],
            options={
                'verbose_name': 'Subscription',
                'verbose_name_plural': 'Subscriptions',
                'unique_together': {('db_character', 'db_key'), ('db_character', 'db_channel'), ('db_channel', 'db_codename')},
            },
        ),
    ]
