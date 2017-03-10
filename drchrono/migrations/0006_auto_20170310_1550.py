# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drchrono', '0005_appointmentmodel_duration'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PatientModel',
        ),
        migrations.RemoveField(
            model_name='appointmentmodel',
            name='duration',
        ),
    ]
