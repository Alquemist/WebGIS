from django.db import models

# Create your models here.

class Bazne(models.Model):
    name = models.CharField(max_length=150, blank=False)
    cell_id = models.CharField(max_length=15, blank=False, primary_key=True)
    lac = models.PositiveIntegerField()
    height = models.FloatField(default=20.0)
    tilit = models.FloatField()
    azimuth = models.FloatField()
    lat = models.CharField(max_length=150,blank=False)
    lon = models.CharField(max_length=150, blank=False)
    beamwdth = models.FloatField(blank=False)
    pow = models.FloatField(blank=False)
    lock = models.BooleanField(blank=False, default=False)


class Roba_s_greskom(models.Model):
    name = models.CharField(max_length=150, blank=True, null=True)
    cell_id = models.CharField(max_length=150, blank=True, null=True)
    lac = models.CharField(max_length=150, blank=True, null=True)
    height = models.CharField(max_length=150, blank=True, null=True)
    tilit = models.CharField(max_length=150, blank=True, null=True)
    azimuth = models.CharField(max_length=150, blank=True, null=True)
    lat = models.CharField(max_length=150, blank=True, null=True)
    lon = models.CharField(max_length=150, blank=True, null=True)
    beamwdth = models.CharField(max_length=150, blank=True, null=True)
    pow = models.CharField(max_length=150, blank=True, null=True)

