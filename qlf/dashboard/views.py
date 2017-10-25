from django.shortcuts import render
from rest_framework import authentication, permissions, viewsets, filters, status
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination

from django.db.models import Max, Min
from django.db.models import Q

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
from django.http import JsonResponse

from django.contrib import messages
import logging

uri = settings.QLF_DAEMON_URL
qlf = Pyro4.Proxy(uri)

uri_manual = settings.QLF_MANUAL_URL
qlf_manual = Pyro4.Proxy(uri_manual)

logger = logging.getLogger(__name__)


class LargeLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 100
    max_limit = 500


class StandartLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 50
    max_limit = 100


class SmallLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 50


class DynamicFieldsMixin(object):

    def list(self, request, *args, **kwargs):
        fields = request.query_params.get('fields', None)

        if fields:
            fields = tuple(fields.split(','))

        queryset = self.filter_queryset(self.get_queryset())

        paginate = request.query_params.get('paginate', None)

        self.pagination_class = StandartLimitOffsetPagination

        if paginate == 'small':
            self.pagination_class = SmallLimitOffsetPagination
        elif paginate == 'large':
            self.pagination_class = LargeLimitOffsetPagination
        elif paginate == 'null':
            self.pagination_class = None

        if self.pagination_class:
            page = self.paginate_queryset(queryset)

            if page is not None:
                serializer = self.get_serializer(page, many=True, fields=fields)
                return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True, fields=fields)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        fields = request.query_params.get('fields', None)

        if fields:
            fields = tuple(fields.split(','))

        instance = self.get_object()
        serializer = self.get_serializer(instance, fields=fields)

        return Response(serializer.data)


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
            process_id = Process.objects.latest('pk').id
        except Process.DoesNotExist as error:
            logger.debug(error)
            process_id = None

        return Process.objects.filter(id=process_id)

    serializer_class = ProcessJobsSerializer


class JobViewSet(DynamicFieldsMixin, DefaultsMixin, viewsets.ModelViewSet):
    """API endpoint for listing jobs"""

    queryset = Job.objects.order_by('start')
    serializer_class = JobSerializer
    filter_fields = ('process',)


class ProcessViewSet(DynamicFieldsMixin, DefaultsMixin, viewsets.ModelViewSet):
    """API endpoint for listing processes"""

    queryset = Process.objects.order_by('start')
    serializer_class = ProcessSerializer
    filter_fields = ('exposure__exposure_id',)


class ConfigurationViewSet(DynamicFieldsMixin, DefaultsMixin, viewsets.ModelViewSet):
    """API endpoint for listing configurations"""

    queryset = Configuration.objects.order_by('creation_date')
    serializer_class = ConfigurationSerializer


class QAViewSet(DynamicFieldsMixin, DefaultsMixin, viewsets.ModelViewSet):
    """API endpoint for listing QA results"""

    filter_fields = ('name',)
    queryset = QA.objects.order_by('name')
    serializer_class = QASerializer

    # def get_queryset(self):
    #     fields = self.request.query_params.get('fields', list())
    #
    #     if fields:
    #         required = ('pk',)
    #         fields = fields.split(',')
    #         fields = list(set(list(required) + fields))
    #         return QA.objects.values(*fields).order_by('name')
    #
    #     return QA.objects.order_by('name')


class ExposureViewSet(DynamicFieldsMixin, DefaultsMixin, viewsets.ModelViewSet):
    """API endpoint for listing exposures"""

    queryset = Exposure.objects.order_by('exposure_id')
    serializer_class = ExposureSerializer


class DataTableExposureViewSet(viewsets.ModelViewSet):
    queryset = Exposure.objects.order_by('exposure_id')
    serializer_class = ExposureSerializer

    ORDER_COLUMN_CHOICES = {
        '0': 'dateobs',
        '1': 'exposure_id',
        '2': 'tile',
        '3': 'telra',
        '4': 'teldec',
        '5': 'exptime',
        '6': 'flavor',
        '7': 'airmass'
    }

    def list(self, request, **kwargs):

        try:
            params = dict(request.query_params)

            start_date = params.get('start_date', [None])[0]
            end_date = params.get('end_date', [None])[0]
            draw = int(params.get('draw', [1])[0])
            length = int(params.get('length', [10])[0])
            start_items = int(params.get('start', [0])[0])
            search_value = params.get('search[value]', [''])[0]
            order_column = params.get('order[0][column]', ['0'])[0]
            order = params.get('order[0][dir]', ['asc'])[0]

            order_column = self.ORDER_COLUMN_CHOICES[order_column]

            # django orm '-' -> desc
            if order == 'desc':
                order_column = '-' + order_column

            if start_date and end_date:
                queryset = Exposure.objects.filter(
                    dateobs__range=(
                        "{} 00:00:00".format(start_date),
                        "{} 23:59:59".format(end_date)
                    )
                )
            else:
                queryset = Exposure.objects

            if search_value:
                queryset = queryset.filter(
                    Q(exposure_id__icontains=search_value) |
                    Q(tile__icontains=search_value) |
                    Q(telra__icontains=search_value) |
                    Q(teldec__icontains=search_value) |
                    Q(flavor__icontains=search_value)
                )

            count = queryset.count()
            queryset = queryset.order_by(order_column)[start_items:start_items + length]

            serializer = ExposureSerializer(queryset, many=True)
            result = dict()
            result['data'] = serializer.data
            result['draw'] = draw
            result['recordsTotal'] = count
            result['recordsFiltered'] = count

            return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)
        except Exception as e:
            return Response(e, status=status.HTTP_404_NOT_FOUND, template_name=None, content_type=None)


class CameraViewSet(DynamicFieldsMixin, DefaultsMixin, viewsets.ModelViewSet):
    """API endpoint for listing cameras"""

    queryset = Camera.objects.order_by('camera')
    serializer_class = CameraSerializer


def start(request):
    qlf_manual_status = qlf_manual.get_status()

    if qlf_manual_status:
        qlf_manual.stop()

    qlf.start()
    return HttpResponseRedirect('dashboard/monitor')


def stop(request):
    qlf.stop()
    return HttpResponseRedirect('dashboard/monitor')


def restart(request):
    qlf_manual_status = qlf_manual.get_status()

    if qlf_manual_status:
        qlf_manual.stop()

    qlf.restart()
    return HttpResponseRedirect('dashboard/monitor')


def daemon_status(request):
    ql_status = True

    run_auto = qlf.get_status()
    run_manual = qlf_manual.get_status()

    if run_auto:
        message = "Please stop the automatic execution before executing the manual processing."
    elif run_manual:
        message = "There is already a sequence of exposures being processed."
    elif qlf.is_running():
        message = "Wait for processing to complete."
    else:
        message = "Ok"
        ql_status = False

    return JsonResponse({'status': ql_status, 'message': message})


def run_manual_mode(request):

    qlf_auto_status = qlf.get_status()

    if qlf_auto_status:
        return JsonResponse({
            "success": False,
            "message": "Please stop the automatic execution before executing the manual processing."
        })

    exposures = request.GET.getlist('exposures[]')
    logger.info(exposures)

    qlf_manual.start(exposures)

    return JsonResponse({
        "success": True,
        "message": "Processing in background."
    })


def observing_history(request):
    exposure = Exposure.objects.all()
    start_date = exposure.aggregate(Min('dateobs'))['dateobs__min']
    end_date = exposure.aggregate(Max('dateobs'))['dateobs__max']

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
