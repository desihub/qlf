from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Job, Metric, Measurement
from django.db import transaction


class MetricSerializer(serializers.ModelSerializer):

    links = serializers.SerializerMethodField()

    class Meta:
        model = Metric
        fields = ('name', 'description', 'units', 'condition',
                  'threshold', 'links',)

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self': reverse('metric-detail', kwargs={'pk': obj.pk},
                            request=request),
         }


class MeasurementSerializer(serializers.ModelSerializer):
    """Serializer for `models.Measurement` objects.

    This serializer is intended to be nested inside the JobSerializer's
    `measurements` field.
    """

    class Meta:
        model = Measurement
        fields = ('metric', 'value')


class JobSerializer(serializers.ModelSerializer):

    links = serializers.SerializerMethodField()

    measurements = MeasurementSerializer(many=True)

    class Meta:
        model = Job
        fields = ('name', 'date', 'status', 'measurements', 'links')

    # Override the create method to create nested objects from request data
    def create(self, data):
        measurements = data.pop('measurements')

        # Use transactions, so that if one of the measurement objects isn't
        # valid that we will rollback even the parent Job object creation
        with transaction.atomic():
            job = Job.objects.create(**data)
            for measurement in measurements:
                Measurement.objects.create(job=job, **measurement)
        return job

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self': reverse('job-detail', kwargs={'pk': obj.pk},
                            request=request),
        }
