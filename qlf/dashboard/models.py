from django.db import models
from json_field import JSONField


class Exposure(models.Model):
    """Exposure information"""

    # TODO: make null=False when exposure data is available

    exposure_id = models.IntegerField(primary_key=True,
                                      help_text='Exposure number')
    telra = models.FloatField(blank=True, null=True,
                              help_text='Central RA of the exposure')
    teldec = models.FloatField(blank=True, null=True,
                               help_text='Central Dec of the exposure')
    tile = models.IntegerField(blank=True, null=True,
                                 help_text='Tile ID')
    dateobs = models.DateTimeField(blank=True, null=True,
                                   help_text='Date of observation')
    flavor = models.CharField(max_length=45, default='Object',
                              help_text='Type of observation')
    night = models.CharField(max_length=45, blank=True,
                             help_text='Night ID', db_index=True)
    airmass = models.FloatField(blank=True, null=True,
                                help_text='Airmass')
    exptime = models.FloatField(blank=True, null=True,
                                help_text='Exposure time')


class Process(models.Model):
    """Process information"""

    STATUS_OK = 0
    STATUS_FAILED = 1

    pipeline_name = models.CharField(max_length=60,
                            help_text='Name of the pipeline.')
    process_dir = models.CharField(max_length=145,
                            help_text='Path to process')
    version = models.CharField(max_length=45,
                            help_text='Path to process')
    start = models.DateTimeField(auto_now=True,
                                help_text='Datetime when the process was started')
    end = models.DateTimeField(blank=True, null=True,
                               help_text='Datetime when the process was finished.')
    status = models.SmallIntegerField(default=STATUS_OK,
                                      help_text='Process status, 0=OK, 1=Failed')
    exposure = models.ForeignKey(Exposure, related_name='process_exposure')


class Configuration(models.Model):
    """Configuration information"""

    configuration = JSONField(decoder=None, help_text='Configuration used.')
    creation_date = models.DateTimeField(auto_now=True,
                                         help_text='Datetime when the configuration was created')
    process = models.ForeignKey(Process, related_name='configuration_process')


class Camera(models.Model):
    """Camera information"""
    camera = models.CharField(max_length=2,
                              help_text='Camera ID', primary_key=True)
    spectrograph = models.CharField(max_length=1,
                                    help_text='Spectrograph ID')
    arm = models.CharField(max_length=1,
                           help_text='Arm ID')

    def __str__(self):
        return str(self.camera)


class Job(models.Model):
    """Job information"""

    STATUS_OK = 0
    STATUS_FAILED = 1
    STATUS_RUNNING = 2

    name = models.CharField(max_length=45, default='Quick Look',
                            help_text='Name of the job.')
    start = models.DateTimeField(auto_now=True,
                                 help_text='Datetime when the job was started')
    end = models.DateTimeField(blank=True, null=True,
                               help_text='Datetime when the job was finished.')
    status = models.SmallIntegerField(default=STATUS_RUNNING,
                                      help_text='Job status, 0=OK, 1=Failed, 2=Running')
    version = models.CharField(max_length=16, null=True, help_text='Version of the pipeline')
    camera = models.ForeignKey(Camera, related_name='camera_jobs')
    process = models.ForeignKey(Process, related_name='process_jobs', on_delete=models.CASCADE)
    logname = models.CharField(max_length=45, null=True,
                               help_text='Name of the log file.')

    def __str__(self):
        return str(self.name)


class QA(models.Model):
    """QA information"""

    name = models.CharField(max_length=45, help_text='QA name')
    description = models.TextField(help_text='QA Description')
    paname = models.CharField(max_length=45, help_text='Associate PA name')
    metric = JSONField(decoder=None, help_text='JSON structure with the QA result')
    job = models.ForeignKey(Job, related_name='job_qas')

    def __str__(self):
        return str(self.name)
