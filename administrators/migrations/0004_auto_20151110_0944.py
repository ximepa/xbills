# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrators', '0003_remove_cuser_date_of_birth'),
    ]

    operations = [
        migrations.AddField(
            model_name='cuser',
            name='first_name',
            field=models.CharField(max_length=30, null=True, verbose_name='first name', blank=True),
        ),
        migrations.AddField(
            model_name='cuser',
            name='last_name',
            field=models.CharField(max_length=30, null=True, verbose_name='last name', blank=True),
        ),
        migrations.AlterField(
            model_name='cuser',
            name='email',
            field=models.EmailField(max_length=255, null=True, verbose_name='email address', blank=True),
        ),
    ]
