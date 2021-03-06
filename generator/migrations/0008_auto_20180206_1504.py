# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-02-06 15:04
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0007_game_sheet_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='map_names_toggle',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='game',
            name='map_transforms',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default='{}'),
        ),
        migrations.AlterField(
            model_name='game',
            name='name',
            field=models.CharField(blank=True, default='New Campaign', max_length=50),
        ),
        migrations.AlterField(
            model_name='game',
            name='scrambler_data',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default='{}'),
        ),
        migrations.AlterField(
            model_name='game',
            name='scrambler_endpoints',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default='{}'),
        ),
    ]
