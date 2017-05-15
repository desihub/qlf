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
                ('camera', models.CharField(help_text='Camera ID', serialize=False, max_length=2, primary_key=True)),
                ('spectrograph', models.CharField(help_text='Spectrograph ID', max_length=1)),
                ('arm', models.CharField(help_text='Arm ID', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('configuration', json_field.fields.JSONField(default='null', help_text='Configuration used.')),
                ('creation_date', models.DateTimeField(help_text='Datetime when the configuration was created', auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Exposure',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('expid', models.CharField(help_text='Exposure number', max_length=8, unique=True)),
                ('telra', models.FloatField(help_text='Central RA of the exposure', blank=True, null=True)),
                ('teldec', models.FloatField(help_text='Central Dec of the exposure', blank=True, null=True)),
                ('tile', models.IntegerField(help_text='Tile ID', blank=True, null=True)),
                ('dateobs', models.DateTimeField(help_text='Date of observation', blank=True, null=True)),
                ('flavor', models.CharField(default='Object', help_text='Type of observation', max_length=45)),
                ('night', models.CharField(help_text='Night ID', blank=True, max_length=45)),
                ('airmass', models.FloatField(help_text='Airmass', blank=True, null=True)),
                ('exptime', models.FloatField(help_text='Exposure time', blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(default='Quick Look', help_text='Name of the job.', max_length=45)),
                ('start', models.DateTimeField(help_text='Datetime when the job was started', auto_now=True)),
                ('end', models.DateTimeField(help_text='Datetime when the job was finished.', blank=True, null=True)),
                ('status', models.SmallIntegerField(default=2, help_text='Job status, 0=OK, 1=Failed, 2=Running')),
                ('version', models.CharField(help_text='Version of the pipeline', max_length=16, null=True)),
                ('logname', models.CharField(help_text='Name of the log file.', max_length=45, null=True)),
                ('camera', models.ForeignKey(to='dashboard.Camera')),
            ],
        ),
        migrations.CreateModel(
            name='Process',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('pipeline_name', models.CharField(help_text='Name of the pipeline.', max_length=60)),
                ('process_dir', models.CharField(help_text='Path to process', max_length=145)),
                ('version', models.CharField(help_text='Path to process', max_length=45)),
                ('start', models.DateTimeField(help_text='Datetime when the process was started', auto_now=True)),
                ('end', models.DateTimeField(help_text='Datetime when the process was finished.', blank=True, null=True)),
                ('status', models.SmallIntegerField(default=0, help_text='Process status, 0=OK, 1=Failed')),
                ('exposure', models.ForeignKey(to='dashboard.Exposure')),
            ],
        ),
        migrations.CreateModel(
            name='QA',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(help_text='QA name', max_length=45)),
                ('description', models.TextField(help_text='QA Description')),
                ('paname', models.CharField(help_text='Associate PA name', max_length=45)),
                ('metric', json_field.fields.JSONField(default='null', help_text='JSON structure with the QA result')),
                ('job', models.ForeignKey(to='dashboard.Job')),
            ],
        ),
        migrations.AddField(
            model_name='job',
            name='process',
            field=models.ForeignKey(to='dashboard.Process'),
        ),
        migrations.AddField(
            model_name='configuration',
            name='process',
            field=models.ForeignKey(to='dashboard.Process'),
        ),
    ]
