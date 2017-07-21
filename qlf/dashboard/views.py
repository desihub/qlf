#from django.shortcuts import render_to_response
from django.shortcuts import render
from rest_framework import authentication, permissions, viewsets, filters, status
from rest_framework.response import Response

from django.db.models import Max, Min
from .models import Job, Exposure, Camera, QA, Process, Configuration
from .serializers import (
    JobSerializer, ExposureSerializer, CameraSerializer,
    QASerializer, ProcessSerializer, ConfigurationSerializer, ProcessJobsSerializer
)
import Pyro4
import datetime

from django.http import HttpResponseRedirect
from django.conf import settings

from bokeh.embed import autoload_server
from django.template import loader
from django.http import HttpResponse

from django.contrib import messages
import logging

uri = settings.QLF_DAEMON_URL
qlf = Pyro4.Proxy(uri)
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

class OHExposureViewSet(viewsets.ModelViewSet):
    """API endpoint for listing exposures"""

    queryset = Exposure.objects.order_by('expid')
    serializer_class = ExposureSerializer

    def list(self, request, **kwargs):

        print('-> DataTables OH')
        print(request.query_params)

        result = dict()
        result['data'] = [{'expid': 2, 'tile': 'testing', 'telra': 344, 'teldec': 65, 'flavor': 'dark'}]
        result['draw'] = 0
        result['recordsTotal'] = 0
        result['recordsFiltered'] = 0
        return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)

        # try:
        #     music = query_exposures_by_args(**request.query_params)
        #     serializer = MusicSerializer(music['items'], many=True)
        #     result = dict()
        #     result['data'] = serializer.data
        #     result['draw'] = music['draw']
        #     result['recordsTotal'] = music['count']
        #     result['recordsFiltered'] = music['count']
        #     return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)
        #
        # except Exception as e:
        #     return Response(e, status=status.HTTP_404_NOT_FOUND, template_name=None, content_type=None)

class CameraViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """API endpoint for listing cameras"""

    queryset = Camera.objects.order_by('camera')
    serializer_class = CameraSerializer

def start(request):
    qlf.start()
    return HttpResponseRedirect('dashboard/monitor')
def stop(request):
    qlf.stop()
    return HttpResponseRedirect('dashboard/monitor')

def restart(request):
    qlf.restart()
    return HttpResponseRedirect('dashboard/monitor')

def observing_history(request):
    start_date = Exposure.objects.all().aggregate(Min('dateobs'))['dateobs__min']
    end_date = Exposure.objects.all().aggregate(Max('dateobs'))['dateobs__max']

    if not start_date and not end_date:
        end_date = start_date = datetime.datetime.now()

    start_date = start_date.strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")

    return render(
        request,
        'dashboard/observing_history.html',
        {
            'start_date': start_date,
            'end_date': end_date
        }
    )

def index(request):
    return render(request, 'dashboard/index.html')

def embed_bokeh(request, bokeh_app):
    """Render the requested app from the bokeh server"""

    # http://bokeh.pydata.org/en/0.12.5/docs/reference/embed.html

    # TODO: test if bokeh server is reachable
    bokeh_script = autoload_server(None, url="{}/{}".format(settings.BOKEH_URL,
                                                            bokeh_app))

    template = loader.get_template('dashboard/embed_bokeh.html')

    context = {'bokeh_script': bokeh_script,
               'bokeh_app': bokeh_app}

    status = qlf.get_status()
    if status == True:
        messages.success(request, "Running")
    elif status == False:
        messages.success(request, "Idle")
    else:
        messages.success(request, "- -")

    response = HttpResponse(template.render(context, request))

    # Save full url path in the HTTP response, so that the bokeh
    # app can use this info

    response.set_cookie('django_full_path', request.get_full_path())
    return response

