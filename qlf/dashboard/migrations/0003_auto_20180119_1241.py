# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import json_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_auto_20171004_1808'),
    ]

    operations = [
        migrations.RenameField(
            model_name='qa',
            old_name='metric',
            new_name='metrics',
        ),
        migrations.AddField(
            model_name='qa',
            name='params',
            field=json_field.fields.JSONField(default='null', help_text='JSON structure with the QA tests'),
        ),
    ]
