# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialnetwork', '0007_relationship'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='content_type',
            field=models.CharField(max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='picture',
            field=models.FileField(null=True, upload_to=b'pictures', blank=True),
            preserve_default=True,
        ),
    ]
