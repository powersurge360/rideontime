# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('multigtfs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StopProxy',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('multigtfs.stop',),
        ),
    ]
