# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialnetwork', '0010_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='picture_url',
            field=models.CharField(max_length=256, blank=True),
            preserve_default=True,
        ),
    ]
