from django.shortcuts import render_to_response
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import authentication, permissions, viewsets, response, filters

from .models import Job, Exposure, Camera, QA
from .serializers import JobSerializer, ExposureSerializer, CameraSerializer, QASerializer
from bokeh.embed import autoload_server


class DefaultsMixin(object):
    """
    Default settings for view authentication, permissions,
    filtering and pagination.
    """

    authentication_classes = (
        authentication.BasicAuthentication,
        authentication.TokenAuthentication,
    )

    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    paginate_by = 25
    paginate_by_param = 'page_size'
    max_paginate_by = 100

    # list of available filter_backends, will enable these for all ViewSets
    filter_backends = (
        filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )


class JobViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """API endpoint for listing jobs"""

    queryset = Job.objects.order_by('date')
    serializer_class = JobSerializer


class QAViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """API endpoint for listing QA results"""

    queryset = QA.objects.order_by('name')
    serializer_class = QASerializer
    filter_fields = ('name',)

class ExposureViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """API endpoint for listing exposures"""

    queryset = Exposure.objects.order_by('expid')
    serializer_class = ExposureSerializer

class CameraViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """API endpoint for listing cameras"""

    queryset = Camera.objects.order_by('camera')
    serializer_class = CameraSerializer


class QaSnrAppViewSet(DefaultsMixin, viewsets.ViewSet):
    """API endpoint for listing bokeh apps"""

    def list(self, request):
        bokeh_script = autoload_server(None, app_path="/qa-snr",
                                       url='default')
        return response.Response({
            'src': bokeh_script.split()[1].split('"')[1],
            'id': bokeh_script.split()[2].split('"')[1]
        })

@ensure_csrf_cookie
def index(request):
    return render_to_response('index.html')
