# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClientUr',
            fields=[
                ('ID', models.AutoField(serialize=False, primary_key=True)),
                ('nazva_ur', models.CharField(max_length=100, null=True, db_column=b'nazva_ur')),
                ('adres_ur', models.CharField(max_length=100, null=True, db_column=b'adres_ur')),
                ('nazva_real', models.CharField(max_length=100, null=True, db_column=b'nazva_real')),
                ('adres_real', models.CharField(max_length=100, null=True, db_column=b'adres_real')),
                ('DRPOU', models.CharField(max_length=13, null=True, db_column=b'DRPOU')),
                ('PDV', models.BooleanField(default=0, db_column=b'PDV')),
                ('IPN', models.CharField(max_length=13, null=True, db_column=b'IPN')),
                ('N_TEL', models.CharField(max_length=10, null=True, db_column=b'N_TEL')),
                ('N_SVID', models.CharField(max_length=50, null=True, db_column=b'N_SVID')),
                ('RAX', models.IntegerField(default=0, db_column=b'RAX')),
                ('BANK', models.CharField(max_length=50, null=True, db_column=b'BANK')),
                ('MFO', models.IntegerField(default=0, db_column=b'MFO')),
                ('Abonplata', models.FloatField(default=0, db_column=b'Abonplata')),
                ('Meggorod', models.FloatField(default=0, db_column=b'Meggorod')),
                ('Dodatkovi', models.FloatField(default=0, db_column=b'Dodatkovi')),
                ('ISDN', models.FloatField(default=0, db_column=b'ISDN')),
                ('Narax', models.FloatField(default=0, db_column=b'Narax')),
                ('Borg', models.FloatField(default=0, db_column=b'Borg')),
                ('propis', models.CharField(max_length=255, null=True, db_column=b'propis')),
                ('Data_DOG', models.DateTimeField(null=True, db_column=b'Data_DOG')),
                ('DOG', models.CharField(max_length=15, null=True, db_column=b'DOG')),
                ('N_TEL1', models.CharField(max_length=10, null=True, db_column=b'N_TEL1')),
            ],
            options={
                'db_table': 'KLIENT_UR',
            },
        ),
        migrations.CreateModel(
            name='TelUr',
            fields=[
                ('N_TELEFON', models.IntegerField(serialize=False, primary_key=True)),
                ('Abonplata', models.FloatField(default=0, db_column=b'Abonplata')),
                ('Meggorod', models.FloatField(default=0, db_column=b'Meggorod')),
                ('Dodatkovi', models.FloatField(default=0, db_column=b'Dodatkovi')),
                ('ID', models.ForeignKey(to='_users.ClientUr')),
            ],
            options={
                'db_table': 'TEL_UR',
            },
        ),
    ]
