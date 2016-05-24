# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrators', '0002_auto_20151110_0927'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cuser',
            name='date_of_birth',
        ),
    ]
