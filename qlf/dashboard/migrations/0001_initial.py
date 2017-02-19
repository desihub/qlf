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
                ('camera', models.CharField(serialize=False, max_length=2, primary_key=True, help_text='Camera ID')),
                ('spectrograph', models.CharField(max_length=1, help_text='Spectrograph ID')),
                ('arm', models.CharField(max_length=1, help_text='Arm ID')),
            ],
        ),
        migrations.CreateModel(
            name='Exposure',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('expid', models.CharField(unique=True, max_length=8, help_text='Exposure number')),
                ('telra', models.FloatField(help_text='Central RA of the exposure', blank=True, null=True)),
                ('teldec', models.FloatField(help_text='Central Dec of the exposure', blank=True, null=True)),
                ('tile', models.IntegerField(help_text='Tile ID', blank=True, null=True)),
                ('dateobs', models.DateTimeField(help_text='Date of observation', blank=True, null=True)),
                ('flavor', models.CharField(default='Object', max_length=45, help_text='Type of observation')),
                ('night', models.CharField(max_length=45, blank=True, help_text='Night ID')),
                ('airmass', models.FloatField(help_text='Airmass', blank=True, null=True)),
                ('exptime', models.FloatField(help_text='Exposure time', blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(default='Quick Look', max_length=45, help_text='Name of the job.')),
                ('date', models.DateTimeField(auto_now=True, help_text='Datetime when the job was registered.')),
                ('status', models.SmallIntegerField(default=0, help_text='Job status, 0=OK, 1=Failed')),
                ('configuration', json_field.fields.JSONField(default='null', help_text='Configuration used.')),
                ('version', models.CharField(max_length=16, help_text='Version of the pipeline')),
            ],
        ),
        migrations.CreateModel(
            name='QA',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=45, help_text='QA name')),
                ('description', models.TextField(help_text='QA Description')),
                ('paname', models.CharField(max_length=45, help_text='Associate PA name')),
                ('value', json_field.fields.JSONField(default='null', help_text='JSON structure with the QA result')),
                ('camera', models.ForeignKey(to='dashboard.Camera')),
            ],
        ),
        migrations.AddField(
            model_name='exposure',
            name='job',
            field=models.ForeignKey(related_name='job', to='dashboard.Job'),
        ),
        migrations.AddField(
            model_name='camera',
            name='exposure',
            field=models.ForeignKey(to='dashboard.Exposure'),
        ),
    ]
