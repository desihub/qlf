from django.db import models
from django.contrib.auth.models import User
from .bokeh_utils import update_bokeh_sessions


class Job(models.Model):
    """Job information"""
    STATUS_OK = 0
    STATUS_FAILED = 1

    name = models.CharField(max_length=32, blank=False,
                               help_text='Name of the Jenkins job')
    date = models.DateTimeField(auto_now=True,
                                help_text='Datetime when job was registered')
    status = models.SmallIntegerField(default=STATUS_OK,
                                      help_text='Job status, 0=OK, 1=Failed')

    def get_jobs(self):
        pass

    def __str__(self):
        return str(self.name)


class Metric(models.Model):
    """QA module information"""
    name = models.CharField(max_length=16, primary_key=True)
    description = models.TextField()
    units = models.CharField(max_length=16)
    condition = models.CharField(max_length=2, blank=False, default='<')
    threshold = models.FloatField(null=False)

    def __str__(self):
        return str(self.name)

class Measurement(models.Model):
    """Measurement of a metric by a job"""
    metric = models.ForeignKey(Metric, null=False)
    job = models.ForeignKey(Job, null=False, related_name='measurements')
    value = models.FloatField(blank=False)

    def __float__(self):
        return str(self.value)

    def save(self, *args, **kwargs):
        super(Measurement, self).save(*args, **kwargs)
        # When a new measurement is saved, update all the data
        # for the bokeh sessions.
        # Improvements:
        # - Only update metrics affected by this data
        # (only get affected Sessions)
        update_bokeh_sessions(UserSession.objects.all())


class UserSession(models.Model):
    user = models.ForeignKey(User, null=False)
    bokehSessionId = models.CharField(max_length=64)


def get_time_series_data(metric):

    m = Measurement.objects.filter(metric=metric)

    if m:
        units = m[0].metric.units
    else:
        units = ""

    return {
            'id': [x.job.pk for x in m],
            'metric': metric,
            'dates': [x.job.date for x in m],
            'values': [x.value for x in m],
            'units':  units,
           }
