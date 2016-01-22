from __future__ import unicode_literals

from django.db import models

class Exposure(models.Model):
    exposure_id = models.AutoField(primary_key=True)
    prop1 = models.IntegerField(default=0)
    prop2 = models.FloatField(default=0.0)

class Spectrograph(models.Model):
    spectrograph_id = models.AutoField(primary_key=True)
    prop1 = models.IntegerField(default=0)
    prop2 = models.FloatField(default=0.0)

class CCD(models.Model):
    ccd_id = models.AutoField(primary_key=True)
    exposure = models.ForeignKey(Exposure, on_delete=models.CASCADE)
    spectrograph = models.ForeignKey(Spectrograph, on_delete=models.CASCADE)
    arm = models.CharField(max_length=200)
    prop1 = models.IntegerField(default=0)
    prop2 = models.FloatField(default=0.0)

class Spectra(models.Model):
    spectra_id = models.AutoField(primary_key=True)
    ccd = models.ForeignKey(CCD, on_delete=models.CASCADE)
    counts = models.IntegerField(default=0)
    sn_ratio = models.FloatField(default=0.0)
    prop1 = models.FloatField(default=0.0)
    prop2 = models.FloatField(default=0.0)

class Fiber(models.Model):
    fiber_id = models.AutoField(primary_key=True)
    spectrograph = models.ForeignKey(Spectrograph, on_delete=models.CASCADE)
    prop1 = models.IntegerField(default=0)
    prop2 = models.FloatField(default=0.0)
