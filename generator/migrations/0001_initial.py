# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-23 23:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('char_name', models.CharField(max_length=200)),
                ('char_sex', models.CharField(choices=[('M', 'male'), ('F', 'female')], max_length=1)),
                ('char_description', models.TextField()),
            ],
        ),
    ]
