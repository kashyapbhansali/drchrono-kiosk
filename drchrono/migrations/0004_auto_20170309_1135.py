# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drchrono', '0003_auto_20170309_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointmentmodel',
            name='status',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
