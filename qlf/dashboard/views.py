from django.shortcuts import render_to_response
from rest_framework import authentication, permissions, viewsets, filters

from .models import Job, Exposure, Camera, QA, Process, Configuration
from .serializers import (
    JobSerializer, ExposureSerializer, CameraSerializer,
    QASerializer, ProcessSerializer, ConfigurationSerializer, ProcessJobsSerializer
)
import Pyro4
from django.http import HttpResponseRedirect
from django.conf import settings

from bokeh.embed import autoload_server
from django.template import loader
from django.http import HttpResponse

import logging

logger = logging.getLogger(__name__)

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


class LastProcessViewSet(viewsets.ModelViewSet):
    """API endpoint for listing last process"""

    def get_queryset(self):
        try:
            last_process = Process.objects.latest('pk').id
        except Process.DoesNotExist as error:
            logger.debug(error)
            last_process = None

        return Process.objects.filter(id=last_process)

    serializer_class = ProcessJobsSerializer


class JobViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """API endpoint for listing jobs"""

    queryset = Job.objects.order_by('start')
    serializer_class = JobSerializer
    filter_fields = ('process',)


class ProcessViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """API endpoint for listing processes"""

    queryset = Process.objects.order_by('start')
    serializer_class = ProcessSerializer


class ConfigurationViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """API endpoint for listing configurations"""

    queryset = Configuration.objects.order_by('creation_date')
    serializer_class = ConfigurationSerializer


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

def start(request):
    uri = "PYRO:qlf.daemon@localhost:56005"
    qlf = Pyro4.Proxy(uri)
    qlf.start()
    return HttpResponseRedirect('dashboard/monitor')

def stop(request):
    uri = "PYRO:qlf.daemon@localhost:56005"
    qlf = Pyro4.Proxy(uri)
    qlf.stop()
    return HttpResponseRedirect('dashboard/monitor')

def restart(request):
    uri = "PYRO:qlf.daemon@localhost:56005"
    qlf = Pyro4.Proxy(uri)
    qlf.restart()
    return HttpResponseRedirect('dashboard/monitor')

def index(request):
    return render_to_response('dashboard/index.html')


def embed_bokeh(request, bokeh_app):
    """Render the requested app from the bokeh server"""

    # http://bokeh.pydata.org/en/0.12.5/docs/reference/embed.html

    # TODO: test if bokeh server is reachable
    bokeh_script = autoload_server(None, url="{}/{}".format(settings.BOKEH_URL,
                                                            bokeh_app))

    template = loader.get_template('dashboard/embed_bokeh.html')

    context = {'bokeh_script': bokeh_script,
               'bokeh_app': bokeh_app}

    response = HttpResponse(template.render(context, request))

    # Save full url path in the HTTP response, so that the bokeh
    # app can use this info

    response.set_cookie('django_full_path', request.get_full_path())
    return response

