# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drchrono', '0004_auto_20170309_1135'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointmentmodel',
            name='duration',
            field=models.IntegerField(default=30),
            preserve_default=False,
        ),
    ]
