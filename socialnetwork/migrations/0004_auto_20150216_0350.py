# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialnetwork', '0003_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='age',
            field=models.IntegerField(max_length=3, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='bio',
            field=models.TextField(max_length=430, null=True),
            preserve_default=True,
        ),
    ]
