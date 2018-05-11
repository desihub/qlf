from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Job, Exposure, Camera, QA, Process, Configuration
from astropy.time import Time
from .utils import get_date
from django.conf import settings
import Pyro4

uri = settings.QLF_DAEMON_URL
qlf = Pyro4.Proxy(uri)


# http://www.django-rest-framework.org/api-guide/serializers/#dynamically-modifying-fields
class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.

    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())

            for field_name in existing - allowed:
                self.fields.pop(field_name)


class QASerializer(DynamicFieldsModelSerializer):

    links = serializers.SerializerMethodField()

    class Meta:
        model = QA
        fields = (
            'pk', 'name', 'description', 'paname',
            'metrics', 'params', 'job', 'links'
        )

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self': reverse('qa-detail', kwargs={'pk': obj.pk},
                            request=request),
         }


class JobSerializer(DynamicFieldsModelSerializer):

    links = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = (
            'pk', 'name', 'start', 'end',
            'status', 'version', 'logname', 'process',
            'camera', 'links'
        )

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self': reverse('job-detail', kwargs={'pk': obj.pk},
                            request=request),
        }


class ProcessSerializer(DynamicFieldsModelSerializer):

    links = serializers.SerializerMethodField()

    class Meta:
        model = Process
        fields = (
            'pk', 'pipeline_name', 'start', 'end',
            'status', 'version', 'process_dir', 'exposure',
            'links'
        )

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self': reverse('process-detail', kwargs={'pk': obj.pk},
                            request=request),
        }


class ExposureSerializer(DynamicFieldsModelSerializer):

    links = serializers.SerializerMethodField()

    class Meta:
        model = Exposure
        fields = (
            'exposure_id', 'tile', 'telra', 'teldec',
            'dateobs', 'exptime', 'flavor', 'night',
            'airmass', 'links'
        )

    def get_links(self, obj):
        return {
            'self': reverse('exposure-detail', kwargs={'pk': obj.pk}),
         }


class CameraSerializer(DynamicFieldsModelSerializer):

    links = serializers.SerializerMethodField()

    class Meta:
        model = Camera
        fields = ('camera', 'spectrograph', 'arm', 'links')

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self': reverse('camera-detail', kwargs={'pk': obj.pk},
                            request=request),
         }


class ConfigurationSerializer(DynamicFieldsModelSerializer):

    links = serializers.SerializerMethodField()

    class Meta:
        model = Configuration
        fields = ('name', 'configuration', 'creation_date', 'links')

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self': reverse('configuration-detail', kwargs={'pk': obj.pk},
                            request=request),
         }


class ProcessJobsSerializer(serializers.ModelSerializer):

    process_jobs = JobSerializer(many=True, read_only=True)

    class Meta:
        model = Process
        fields = ('id', 'exposure', 'process_jobs')


class ProcessingHistoryExposureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exposure
        fields = (
            'exposure_id', 'tile', 'telra', 'teldec',
            'dateobs', 'exptime', 'flavor', 'night',
            'airmass'
        )


class ProcessingHistorySerializer(DynamicFieldsModelSerializer):

    runtime = serializers.SerializerMethodField()
    datemjd = serializers.SerializerMethodField()
    exposure = ProcessingHistoryExposureSerializer(required=True)

    class Meta:
        model = Process
        fields = (
            'pk',
            'exposure',
            'datemjd',
            'runtime',
            'start',
            'end',
        )

    def get_runtime(self, obj):
        if obj.end is not None and obj.start is not None:
            return str(obj.end.replace(microsecond=0) - obj.start.replace(microsecond=0))
        else:
            return None

    def get_datemjd(self, obj):
        time = get_date(obj.exposure_id)
        if time is None:
            return None
        else:
            return time.mjd


class SingleQASerializer(DynamicFieldsModelSerializer):

    datemjd = serializers.SerializerMethodField()
    qa_tests = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()

    class Meta:
        model = Process
        fields = ('pk', 'date', 'exposure_id', 'datemjd', 'qa_tests')

    def get_datemjd(self, obj):
        time = get_date(obj.exposure_id)
        if time is None:
            return None
        else:
            return time.mjd

    def get_date(self, obj):
        return obj.exposure.dateobs

    def get_qa_tests(self, obj):
        return qlf.qa_tests(obj.pk)


class ObservingHistorySerializer(DynamicFieldsModelSerializer):

    datemjd = serializers.SerializerMethodField()
    last_exposure_process_id = serializers.SerializerMethodField()

    class Meta:
        model = Exposure
        fields = (
            'exposure_id',
            'dateobs',
            'datemjd',
            'tile',
            'telra',
            'teldec',
            'exptime',
            'airmass',
            'last_exposure_process_id',
            'flavor'
        )

    def get_datemjd(self, obj):
        time = get_date(obj.pk)
        if time is None:
            return None
        else:
            return time.mjd

    def get_last_exposure_process_id(self, obj):
        return Process.objects.all().filter(exposure=obj.pk).last().pk


class ExposuresDateRangeSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Exposure
        fields = ('exposure_id', 'dateobs')


class ExposureFlavorSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Exposure
        fields = ('flavor',)
