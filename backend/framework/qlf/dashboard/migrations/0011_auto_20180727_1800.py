# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-27 18:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0010_auto_20180718_1945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='process',
            name='configuration',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='process_configuration', to='dashboard.Configuration'),
        ),
    ]