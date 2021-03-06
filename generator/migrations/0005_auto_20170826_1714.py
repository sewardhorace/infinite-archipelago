# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-26 17:14
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('generator', '0004_credentialsmodel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='user',
        ),
        migrations.RemoveField(
            model_name='game',
            name='profile',
        ),
        migrations.AddField(
            model_name='game',
            name='scrambler_data',
            field=django.contrib.postgres.fields.jsonb.JSONField(default='{}'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='scrambler_endpoints',
            field=django.contrib.postgres.fields.jsonb.JSONField(default='{}'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='user',
            field=models.OneToOneField(default=2, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='credentialsmodel',
            name='id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
