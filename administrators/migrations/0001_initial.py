# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import re
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('username', models.CharField(help_text='Required. 30 characters or fewer. Letters, numbers and @/./+/-/_ characters', unique=True, max_length=30, verbose_name=b'username', validators=[django.core.validators.RegexValidator(re.compile(b'^[\\w.@+-]+$'), b'Enter a valid username.', b'invalid')])),
                ('email', models.EmailField(max_length=255, verbose_name='email address')),
                ('date_of_birth', models.DateField()),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('receive_newsletter', models.BooleanField(default=False, verbose_name='receive newsletter')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
        ),
    ]
