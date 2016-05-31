# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=32, help_text='Name of the Jenkins job')),
                ('date', models.DateTimeField(auto_now=True, help_text='Datetime when job was registered')),
                ('status', models.SmallIntegerField(default=0, help_text='Job status, 0=OK, 1=Failed')),
            ],
        ),
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('value', models.FloatField()),
                ('job', models.ForeignKey(related_name='measurements', to='dashboard.Job')),
            ],
        ),
        migrations.CreateModel(
            name='Metric',
            fields=[
                ('name', models.CharField(serialize=False, max_length=16, primary_key=True)),
                ('description', models.TextField()),
                ('units', models.CharField(max_length=16)),
                ('condition', models.CharField(default='<', max_length=2)),
                ('threshold', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='UserSession',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('bokehSessionId', models.CharField(max_length=64)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='measurement',
            name='metric',
            field=models.ForeignKey(to='dashboard.Metric'),
        ),
    ]
