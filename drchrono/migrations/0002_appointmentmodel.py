# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drchrono', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppointmentModel',
            fields=[
                ('id', models.CharField(max_length=10, serialize=False, primary_key=True)),
                ('doctor', models.IntegerField()),
                ('patient', models.IntegerField()),
                ('office', models.IntegerField()),
                ('exam_room', models.IntegerField()),
                ('reason', models.CharField(max_length=1000, blank=True)),
                ('status', models.CharField(max_length=20)),
                ('deleted_flag', models.BooleanField()),
                ('scheduled_time', models.DateTimeField()),
                ('arrival_time', models.DateTimeField(blank=True)),
                ('call_in_time', models.DateTimeField(blank=True)),
            ],
        ),
    ]
