from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Job, Exposure, Camera, QA


class QASerializer(serializers.ModelSerializer):

    links = serializers.SerializerMethodField()

    class Meta:
        model = QA
        fields = ('name', 'description', 'paname', 'value', 'links')

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self': reverse('qa-detail', kwargs={'pk': obj.pk},
                            request=request),
         }


class JobSerializer(serializers.ModelSerializer):

    links = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = ('name', 'date', 'status', 'configuration', 'links')

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self': reverse('job-detail', kwargs={'pk': obj.pk},
                            request=request),
        }


class ExposureSerializer(serializers.ModelSerializer):

    links = serializers.SerializerMethodField()

    class Meta:
        model = Exposure
        fields = ('expid', 'flavor', 'links')

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



