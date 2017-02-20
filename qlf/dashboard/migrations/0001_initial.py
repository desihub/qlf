# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import json_field.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Camera',
            fields=[
                ('camera', models.CharField(primary_key=True, help_text='Camera ID', max_length=2, serialize=False)),
                ('spectrograph', models.CharField(help_text='Spectrograph ID', max_length=1)),
                ('arm', models.CharField(help_text='Arm ID', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Exposure',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('expid', models.CharField(unique=True, help_text='Exposure number', max_length=8)),
                ('telra', models.FloatField(null=True, help_text='Central RA of the exposure', blank=True)),
                ('teldec', models.FloatField(null=True, help_text='Central Dec of the exposure', blank=True)),
                ('tile', models.IntegerField(null=True, help_text='Tile ID', blank=True)),
                ('dateobs', models.DateTimeField(null=True, help_text='Date of observation', blank=True)),
                ('flavor', models.CharField(help_text='Type of observation', max_length=45, default='Object')),
                ('night', models.CharField(help_text='Night ID', max_length=45, blank=True)),
                ('airmass', models.FloatField(null=True, help_text='Airmass', blank=True)),
                ('exptime', models.FloatField(null=True, help_text='Exposure time', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(help_text='Name of the job.', max_length=45, default='Quick Look')),
                ('date', models.DateTimeField(auto_now=True, help_text='Datetime when the job was registered.')),
                ('status', models.SmallIntegerField(help_text='Job status, 0=OK, 1=Failed', default=0)),
                ('configuration', json_field.fields.JSONField(help_text='Configuration used.', default='null')),
                ('version', models.CharField(help_text='Version of the pipeline', max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='QA',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(unique=True, help_text='QA name', max_length=45)),
                ('description', models.TextField(help_text='QA Description')),
                ('paname', models.CharField(help_text='Associate PA name', max_length=45)),
                ('value', json_field.fields.JSONField(help_text='JSON structure with the QA result', default='null')),
                ('camera', models.ForeignKey(to='dashboard.Camera')),
            ],
        ),
        migrations.AddField(
            model_name='exposure',
            name='job',
            field=models.ForeignKey(to='dashboard.Job', related_name='job'),
        ),
        migrations.AddField(
            model_name='camera',
            name='exposure',
            field=models.ForeignKey(to='dashboard.Exposure'),
        ),
    ]
