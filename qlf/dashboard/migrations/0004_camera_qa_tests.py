# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import json_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_auto_20180119_1241'),
    ]

    operations = [
        migrations.AddField(
            model_name='camera',
            name='qa_tests',
            field=json_field.fields.JSONField(default='null', help_text='JSON structure with the QA tests results'),
        ),
    ]
