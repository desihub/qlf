from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Job, Exposure, Camera, QA, Process, Configuration


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
            'metric', 'job', 'links'
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
        fields = ('configuration', 'creation_date', 'links')

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


