# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('multigtfs', '0001_initial'),
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RouteProxy',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('multigtfs.route',),
        ),
        migrations.CreateModel(
            name='ServiceProxy',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('multigtfs.service',),
        ),
        migrations.CreateModel(
            name='StopTimeProxy',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('multigtfs.stoptime',),
        ),
        migrations.CreateModel(
            name='TripProxy',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('multigtfs.trip',),
        ),
    ]
