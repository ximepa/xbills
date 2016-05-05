# -*- encoding: utf-8 -*-
__author__ = 'ximepa'

from django.db import models


class ClientUr(models.Model):
    ID = models.AutoField(primary_key=True)
    nazva_ur = models.CharField(max_length=100, null=True, db_column='nazva_ur')
    adres_ur = models.CharField(max_length=100, null=True, db_column='adres_ur')
    nazva_real = models.CharField(max_length=100, null=True, db_column='nazva_real')
    adres_real = models.CharField(max_length=100, null=True, db_column='adres_real')
    DRPOU = models.CharField(max_length=13, null=True, db_column='DRPOU')
    PDV = models.BooleanField(default=0, db_column='PDV')
    IPN = models.CharField(max_length=13, null=True, db_column='IPN')
    N_TEL = models.CharField(max_length=10, null=True, db_column='N_TEL')
    N_SVID = models.CharField(max_length=50, null=True, db_column='N_SVID')
    RAX = models.IntegerField(default=0, db_column='RAX')
    BANK = models.CharField(max_length=50, null=True, db_column='BANK')
    MFO = models.IntegerField(default=0, db_column='MFO')
    Abonplata = models.FloatField(default=0, db_column='Abonplata')
    Meggorod = models.FloatField(default=0, db_column='Meggorod')
    Dodatkovi = models.FloatField(default=0, db_column='Dodatkovi')
    ISDN = models.FloatField(default=0, db_column='ISDN')
    Narax = models.FloatField(default=0, db_column='Narax')
    Borg = models.FloatField(default=0, db_column='Borg')
    propis = models.CharField(max_length=255, null=True, db_column='propis')
    Data_DOG = models.DateTimeField(null=True, db_column='Data_DOG')
    DOG = models.CharField(max_length=15, null=True, db_column='DOG')
    N_TEL1 = models.CharField(max_length=10, null=True, db_column='N_TEL1')

    def __unicode__(self):
        return '%s' % (self.nazva_ur)

    class Meta:
        db_table = 'KLIENT_UR'


class TelUr(models.Model):
    ID = models.ForeignKey('ClientUr')
    N_TELEFON = models.IntegerField(primary_key=True)
    Abonplata = models.FloatField(default=0, db_column='Abonplata')
    Meggorod = models.FloatField(default=0, db_column='Meggorod')
    Dodatkovi = models.FloatField(default=0, db_column='Dodatkovi')

    def __unicode__(self):
        return '%s' % (self.ID)

    class Meta:
        db_table = 'TEL_UR'