# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drchrono', '0002_appointmentmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointmentmodel',
            name='arrival_time',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='appointmentmodel',
            name='call_in_time',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
