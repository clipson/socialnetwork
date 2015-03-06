# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialnetwork', '0005_auto_20150217_2116'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='content_type',
            field=models.CharField(max_length=50, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='picture',
            field=models.FileField(upload_to=b'pictures', blank=True),
            preserve_default=True,
        ),
    ]
