# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PatientModel',
            fields=[
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('doctor_id', models.IntegerField()),
                ('gender', models.CharField(max_length=10)),
                ('birthday', models.DateField(default=datetime.date)),
                ('patient_id', models.IntegerField(serialize=False, primary_key=True)),
                ('patient_email', models.EmailField(default=b'', max_length=254)),
            ],
        ),
    ]
