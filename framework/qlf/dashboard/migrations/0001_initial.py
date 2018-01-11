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
            name='Configuration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('configuration', json_field.fields.JSONField(help_text='Configuration used.', default='null')),
                ('creation_date', models.DateTimeField(auto_now=True, help_text='Datetime when the configuration was created')),
            ],
        ),
        migrations.CreateModel(
            name='Exposure',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('expid', models.CharField(unique=True, help_text='Exposure number', max_length=8)),
                ('telra', models.FloatField(blank=True, null=True, help_text='Central RA of the exposure')),
                ('teldec', models.FloatField(blank=True, null=True, help_text='Central Dec of the exposure')),
                ('tile', models.IntegerField(blank=True, null=True, help_text='Tile ID')),
                ('dateobs', models.DateTimeField(blank=True, null=True, help_text='Date of observation')),
                ('flavor', models.CharField(help_text='Type of observation', max_length=45, default='Object')),
                ('night', models.CharField(blank=True, help_text='Night ID', max_length=45)),
                ('airmass', models.FloatField(blank=True, null=True, help_text='Airmass')),
                ('exptime', models.FloatField(blank=True, null=True, help_text='Exposure time')),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(help_text='Name of the job.', max_length=45, default='Quick Look')),
                ('start', models.DateTimeField(auto_now=True, help_text='Datetime when the job was started')),
                ('end', models.DateTimeField(blank=True, null=True, help_text='Datetime when the job was finished.')),
                ('status', models.SmallIntegerField(help_text='Job status, 0=OK, 1=Failed, 2=Running', default=2)),
                ('version', models.CharField(null=True, max_length=16, help_text='Version of the pipeline')),
                ('logname', models.CharField(null=True, max_length=45, help_text='Name of the log file.')),
                ('camera', models.ForeignKey(to='dashboard.Camera')),
            ],
        ),
        migrations.CreateModel(
            name='Process',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('pipeline_name', models.CharField(help_text='Name of the pipeline.', max_length=60)),
                ('process_dir', models.CharField(help_text='Path to process', max_length=145)),
                ('version', models.CharField(help_text='Path to process', max_length=45)),
                ('start', models.DateTimeField(auto_now=True, help_text='Datetime when the process was started')),
                ('end', models.DateTimeField(blank=True, null=True, help_text='Datetime when the process was finished.')),
                ('status', models.SmallIntegerField(help_text='Process status, 0=OK, 1=Failed', default=0)),
                ('exposure', models.ForeignKey(to='dashboard.Exposure')),
            ],
        ),
        migrations.CreateModel(
            name='QA',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(help_text='QA name', max_length=45)),
                ('description', models.TextField(help_text='QA Description')),
                ('paname', models.CharField(help_text='Associate PA name', max_length=45)),
                ('metric', json_field.fields.JSONField(help_text='JSON structure with the QA result', default='null')),
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
