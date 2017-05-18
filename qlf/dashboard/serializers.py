from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Job, Exposure, Camera, QA, Process, Configuration


class QASerializer(serializers.ModelSerializer):

    links = serializers.SerializerMethodField()

    class Meta:
        model = QA
        fields = ('name', 'description', 'paname', 'metric', 'links')

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self': reverse('qa-detail', kwargs={'pk': obj.pk},
                            request=request),
         }

class JobSerializer(serializers.ModelSerializer):

    links = serializers.SerializerMethodField()
    process = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = ('name', 'start', 'end', 'status', 'version', 'logname', 'process', 'links')

    def get_process(self, obj):
        return obj.process.pk


    def get_links(self, obj):
        request = self.context['request']
        return {
            'self': reverse('job-detail', kwargs={'pk': obj.pk},
                            request=request),
        }

class MonitorSerializer(serializers.ModelSerializer):

    links = serializers.SerializerMethodField()
    process = serializers.SerializerMethodField()
    exposure = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = ('process', 'exposure', 'logname', 'links')

    def get_exposure(self, obj):

        return obj.process.exposure_id

    def get_process(self, obj):

        return obj.process.pk


    def get_links(self, obj):
        request = self.context['request']
        return {
            'self': reverse('job-detail', kwargs={'pk': obj.pk},
                            request=request),
        }


class ProcessSerializer(serializers.ModelSerializer):

    links = serializers.SerializerMethodField()

    class Meta:
        model = Process
        fields = ('pipeline_name', 'start', 'end', 'status', 'version', 'process_dir', 'links')

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self': reverse('process-detail', kwargs={'pk': obj.pk},
                            request=request),
        }

class ExposureSerializer(serializers.ModelSerializer):

    links = serializers.SerializerMethodField()

    class Meta:
        model = Exposure
        fields = ('expid', 'flavor', 'links',)

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self': reverse('exposure-detail', kwargs={'pk': obj.pk},
                            request=request),
         }

class CameraSerializer(serializers.ModelSerializer):

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

class ConfigurationSerializer(serializers.ModelSerializer):

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


