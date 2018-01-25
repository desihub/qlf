# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exposure',
            name='expid',
        ),
        migrations.RemoveField(
            model_name='exposure',
            name='id',
        ),
        migrations.AddField(
            model_name='exposure',
            name='exposure_id',
            field=models.IntegerField(serialize=False, default=None, primary_key=True, help_text='Exposure number'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='configuration',
            name='process',
            field=models.ForeignKey(to='dashboard.Process', related_name='configuration_process'),
        ),
        migrations.AlterField(
            model_name='exposure',
            name='night',
            field=models.CharField(blank=True, help_text='Night ID', db_index=True, max_length=45),
        ),
        migrations.AlterField(
            model_name='job',
            name='camera',
            field=models.ForeignKey(to='dashboard.Camera', related_name='camera_jobs'),
        ),
        migrations.AlterField(
            model_name='job',
            name='process',
            field=models.ForeignKey(to='dashboard.Process', related_name='process_jobs'),
        ),
        migrations.AlterField(
            model_name='process',
            name='exposure',
            field=models.ForeignKey(to='dashboard.Exposure', related_name='process_exposure'),
        ),
        migrations.AlterField(
            model_name='qa',
            name='job',
            field=models.ForeignKey(to='dashboard.Job', related_name='job_qas'),
        ),
    ]
