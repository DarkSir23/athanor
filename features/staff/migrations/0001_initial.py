# Generated by Django 2.2.6 on 2019-11-23 03:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('characters', '0012_merge_20191110_2125'),
    ]

    operations = [
        migrations.CreateModel(
            name='StaffCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=255, unique=True)),
                ('order', models.PositiveSmallIntegerField(default=0, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='StaffEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveSmallIntegerField(default=0)),
                ('position', models.CharField(blank=True, max_length=255, null=True)),
                ('duty', models.CharField(blank=True, default='On', max_length=255, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('vacation', models.DateTimeField(null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='staffers', to='staff.StaffCategory')),
                ('character', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='characters.ObjectDB')),
            ],
        ),
    ]
