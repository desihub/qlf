from django.shortcuts import render
from rest_framework import (
    authentication, permissions, viewsets, filters,
    status, views
)
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination

from django.db.models import Max, Min
# from django.db.models import Q

from .models import Job, Exposure, Camera, QA, Process, Configuration, ProcessComment
from .serializers import (
    JobSerializer, ExposureSerializer, CameraSerializer,
    QASerializer, ProcessSerializer, ConfigurationSerializer,
    ProcessJobsSerializer, ProcessingHistorySerializer,
    ObservingHistorySerializer, ExposuresDateRangeSerializer,
    ExposureFlavorSerializer, ProcessCommentSerializer,
    ExposureNightSerializer
)

from datetime import datetime, timedelta

from django.http import HttpResponseRedirect
from django.conf import settings

from bokeh.embed import server_document
from django.template import loader
from django.http import HttpResponse
from django.http import JsonResponse

from dashboard.bokeh.fits2png.fits2png import Fits2png
from dashboard.bokeh.qacountpix.main import Countpix
from dashboard.bokeh.qagetbias.main import Bias
from dashboard.bokeh.qagetrms.main import RMS
from dashboard.bokeh.qaxwsigma.main import Xwsigma
from dashboard.bokeh.qacountbins.main import Countbins
from dashboard.bokeh.qaskycont.main import Skycont
from dashboard.bokeh.qaskypeak.main import Skypeak
from dashboard.bokeh.qainteg.main import Integ
from dashboard.bokeh.qaskyresid.main import Skyresid
from dashboard.bokeh.qasnr.main import SNR
from dashboard.bokeh.globalfiber.main import GlobalFiber
from dashboard.bokeh.globalfocus.main import GlobalFocus

from .filters import ProcessingHistoryFilter

from django.core.mail import send_mail
import os

from clients import get_exposure_monitoring

from django.contrib import messages
import logging

from util import get_config

from .config_file import edit_qlf_config_file, set_default_configuration

qlf = get_exposure_monitoring()

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
                serializer = self.get_serializer(
                    page, many=True, fields=fields)
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


class ProcessingHistoryViewSet(DynamicFieldsMixin, DefaultsMixin, viewsets.ModelViewSet):
    """API endpoint for listing processing history"""

    queryset = Process.objects.order_by('-pk')
    serializer_class = ProcessingHistorySerializer
    filter_class = ProcessingHistoryFilter
    ordering_fields = (
        'pk',
        'exposure_id',
        'start',
        'exposure__tile',
        'exposure__telra',
        'exposure__night',
        'exposure__exptime',
        'exposure__flavor',
        'exposure__program',
        'exposure__dateobs',
        'exposure__airmass',
        'exposure__teldec')

    # Added to filter datemin and datemax
    def list(self, request, *args, **kwargs):
        response = super(ProcessingHistoryViewSet, self).list(
            request, args, kwargs)
        datemin = request.query_params.get('datemin')
        datemax = request.query_params.get('datemax')
        queryset = self.filter_queryset(self.get_queryset())
        if datemax and datemin:
            try:
                datemin = datetime.strptime(datemin, "%Y-%m-%d")
                datemax = datetime.strptime(
                    datemax, "%Y-%m-%d") + timedelta(days=1)
                queryset = queryset.filter(exposure__dateobs__gte=datemin)
                queryset = queryset.filter(exposure__dateobs__lte=datemax)
            except:
                response.data['results'] = {"Error": 'wrong date format'}
                return response

        if self.pagination_class:
            page = self.paginate_queryset(queryset)

            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ObservingHistoryViewSet(DynamicFieldsMixin, DefaultsMixin, viewsets.ModelViewSet):
    """API endpoint for listing observing history"""

    queryset = Exposure.objects.order_by('-pk')
    serializer_class = ObservingHistorySerializer
    filter_fields = ('exposure_id', 'flavor', 'night',)

    # Added to order SerializerMethodFields
    def list(self, request, *args, **kwargs):
        response = super(ObservingHistoryViewSet, self).list(
            request, args, kwargs)
        datemin = request.query_params.get('datemin')
        datemax = request.query_params.get('datemax')
        queryset = self.filter_queryset(self.get_queryset())
        if datemax and datemin:
            try:
                datemin = datetime.strptime(datemin, "%Y-%m-%d")
                datemax = datetime.strptime(
                    datemax, "%Y-%m-%d") + timedelta(days=1)
                queryset = queryset.filter(dateobs__gte=datemin)
                queryset = queryset.filter(dateobs__lte=datemax)
            except:
                response.data['results'] = {"Error": 'wrong date format'}
                return response
        if self.pagination_class:
            page = self.paginate_queryset(queryset)

            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class JobViewSet(DynamicFieldsMixin, DefaultsMixin, viewsets.ModelViewSet):
    """API endpoint for listing jobs"""

    queryset = Job.objects.order_by('start')
    serializer_class = JobSerializer
    filter_fields = ('process',)


class ProcessViewSet(DynamicFieldsMixin, DefaultsMixin, viewsets.ModelViewSet):
    """API endpoint for listing processes"""

    queryset = Process.objects.order_by('start')
    serializer_class = ProcessSerializer
    filter_fields = ('exposure',)


class ConfigurationViewSet(DynamicFieldsMixin, DefaultsMixin, viewsets.ModelViewSet):
    """API endpoint for listing configurations"""

    queryset = Configuration.objects.order_by('creation_date')
    serializer_class = ConfigurationSerializer


class CurrentConfigurationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Configuration.objects.order_by('creation_date')
    serializer_class = ConfigurationSerializer

    def list(self, request, *args, **kwargs):
        response = super(CurrentConfigurationViewSet, self).list(
            request, args, kwargs)
        cfg = get_config()
        configuration = dict(
            base_exposures_path=cfg.get("namespace", "base_exposures_path"),
            min_interval=cfg.get("main", "min_interval"),
            max_interval=cfg.get("main", "max_interval"),
            allowed_delay=cfg.get("main", "allowed_delay"),
            max_exposures=cfg.get("main", "max_exposures"),
            max_nights=cfg.get("main", "max_nights"),
            logfile=cfg.get("main", "logfile"),
            loglevel=cfg.get("main", "loglevel"),
            logpipeline=cfg.get("main", "logpipeline"),
            qlconfig=cfg.get("main", "qlconfig"),
            night=cfg.get("data", "night"),
            exposures=cfg.get("data", "exposures"),
            arms=cfg.get("data", "arms"),
            spectrographs=cfg.get("data", "spectrographs"),
            desi_spectro_data=cfg.get("namespace", "desi_spectro_data"),
            desi_spectro_redux=cfg.get("namespace", "desi_spectro_redux"),
            calibration_path=cfg.get("namespace", "calibration_path")
        )
        response.data = {'results': configuration}
        return response


class QlConfigViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Configuration.objects.order_by('creation_date')
    serializer_class = ConfigurationSerializer

    def list(self, request, *args, **kwargs):
        response = super(QlConfigViewSet, self).list(
            request, args, kwargs)
        try:
            cfg = get_config()
            ql_type = request.GET.get('type')
            ql_path = cfg.get("main", "qlconfig")
            with open(ql_path.format(ql_type)) as f:
                qlconfig = f.read()
        except Exception as err:
            logger.info(err)
            qlconfig = 'Error reading qlconfig: {}'.format(err)
        response.data = qlconfig
        return response


class QlCalibrationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Configuration.objects.order_by('creation_date')
    serializer_class = ConfigurationSerializer

    def list(self, request, *args, **kwargs):
        response = super(QlCalibrationViewSet, self).list(
            request, args, kwargs)
        calibration = qlf.get_calibration()
        response.data = calibration
        return response


class SetConfigurationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Configuration.objects.order_by('creation_date')
    serializer_class = ConfigurationSerializer

    def list(self, request, *args, **kwargs):
        response = super(SetConfigurationViewSet, self).list(
            request, args, kwargs)
        configuration = request.GET.get('configuration')
        if configuration is not None:
            qlf.set_current_configuration(configuration)
            response.data = {'status': 'Configuration set'}
            return response
        else:
            response.data = {'Error': 'Missing configuration'}
            return response


class QAViewSet(DynamicFieldsMixin, DefaultsMixin, viewsets.ModelViewSet):
    """API endpoint for listing QA results"""

    filter_fields = ('name',)
    queryset = QA.objects.order_by('name')
    serializer_class = QASerializer


class ExposureViewSet(DynamicFieldsMixin, DefaultsMixin, viewsets.ModelViewSet):
    """API endpoint for listing exposures"""

    queryset = Exposure.objects.order_by('exposure_id')
    serializer_class = ExposureSerializer
    filter_fields = ('exposure_id',)


class DistinctFlavorsViewSet(DynamicFieldsMixin, DefaultsMixin, viewsets.ModelViewSet):
    """API endpoint for listing exposures flavors"""

    queryset = Exposure.objects.all().distinct('flavor')
    serializer_class = ExposureFlavorSerializer


class DistinctNightsViewSet(DynamicFieldsMixin, DefaultsMixin, viewsets.ModelViewSet):
    """API endpoint for listing exposures distinct nights"""

    queryset = Exposure.objects.all().distinct('night')
    serializer_class = ExposureNightSerializer


class AddExposureViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Process.objects.none()
    serializer_class = ProcessSerializer

    def list(self, request, *args, **kwargs):
        response = super(AddExposureViewSet, self).list(
            request, args, kwargs)
        exposure_id = request.GET.get('exposure_id')
        if exposure_id is not None:
            qlf.add_exposures([exposure_id])
            response.data = {'status': 'Exposure added to queue'}
            return response
        else:
            response.data = {'Error': 'Missing exposure_id'}
            return response


class ExposuresDateRangeViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for listing exposures date range"""
    queryset = Exposure.objects.order_by('exposure_id')

    def list(self, request, *args, **kwargs):
        response = super(ExposuresDateRangeViewSet, self).list(
            request, args, kwargs)
        queryset = self.get_queryset()
        start_date = queryset.aggregate(Min('dateobs'))['dateobs__min']
        end_date = queryset.aggregate(Max('dateobs'))['dateobs__max']
        response.data = {"start_date": start_date, "end_date": end_date}
        return response

    serializer_class = ExposuresDateRangeSerializer


class CameraViewSet(DynamicFieldsMixin, DefaultsMixin, viewsets.ModelViewSet):
    """API endpoint for listing cameras"""

    queryset = Camera.objects.order_by('camera')
    serializer_class = CameraSerializer


class ProcessCommentViewSet(DynamicFieldsMixin, DefaultsMixin, viewsets.ModelViewSet):
    """API endpoint for listing comments"""

    queryset = ProcessComment.objects.order_by('-pk')
    serializer_class = ProcessCommentSerializer
    permission_classes = [permissions.AllowAny]
    filter_fields = ('process',)


def start(request):
    qlf.start()
    return HttpResponseRedirect('dashboard/monitor')


def stop(request):
    qlf.stop()

    return HttpResponseRedirect('dashboard/monitor')


def reset(request):
    qlf.reset()
    return HttpResponseRedirect('dashboard/monitor')


def daemon_status(request):
    ql_status = True

    run_auto = qlf.get_status()
    # run_manual = qlf_manual.get_status()
    run_manual = None

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

    # qlf_manual.start(exposures)

    return JsonResponse({
        "success": True,
        "message": "Processing in background."
    })


def index(request):
    return render(request, 'dashboard/index.html')


def embed_bokeh(request, bokeh_app):
    """Render the requested app from the bokeh server"""

    # http://bokeh.pydata.org/en/0.12.5/docs/reference/embed.html

    # TODO: test if bokeh server is reachable
    bokeh_script = server_document(arguments=request.GET, url="{}/{}".format(settings.BOKEH_URL,
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


def fits_to_png(request):
    """Generates and render png"""
    template = loader.get_template('dashboard/fits_to_png.html')
    # Generate Image
    cam = request.GET.get('cam')
    processing = request.GET.get('processing')
    process_id = request.GET.get('process')
    process = Process.objects.get(pk=process_id)
    night = process.exposure.night
    exposure_id = process.exposure_id
    png_image = Fits2png(cam, processing, night,
                         exposure_id).convert_fits2png()
    context = {'image': png_image}
    response = HttpResponse(template.render(context, request))

    return response


def load_qa(request):
    """Generates and render png"""
    template = loader.get_template('dashboard/qa.html')
    # Generate Image
    qa = request.GET.get('qa')
    spectrograph = request.GET.get('spectrograph')
    process_id = request.GET.get('process_id')
    arm = request.GET.get('arm')
    try:
        if qa == 'qacountpix':
            qa_html = Countpix(process_id, arm, spectrograph).load_qa()
        elif qa == 'qagetbias':
            qa_html = Bias(process_id, arm, spectrograph).load_qa()
        elif qa == 'qagetrms':
            qa_html = RMS(process_id, arm, spectrograph).load_qa()
        elif qa == 'qaxwsigma':
            qa_html = Xwsigma(process_id, arm, spectrograph).load_qa()
        elif qa == 'qacountbins':
            qa_html = Countbins(process_id, arm, spectrograph).load_qa()
        elif qa == 'qaskycont':
            qa_html = Skycont(process_id, arm, spectrograph).load_qa()
        elif qa == 'qaskypeak':
            qa_html = Skypeak(process_id, arm, spectrograph).load_qa()
        elif qa == 'qainteg':
            qa_html = Integ(process_id, arm, spectrograph).load_qa()
        elif qa == 'qaskyresid':
            qa_html = Skyresid(process_id, arm, spectrograph).load_qa()
        elif qa == 'qasnr':
            qa_html = SNR(process_id, arm, spectrograph).load_qa()
        elif qa == 'globalfiber':
            qa_html = GlobalFiber(process_id, arm, spectrograph).load_qa()
        elif qa == 'globalfocus':
            qa_html = GlobalFocus(process_id, arm, spectrograph).load_qa()
        else:
            qa_html = "Couldn't load QA"
    except:
        qa_html = "Can't load QA"

    context = {'image': qa_html}
    response = HttpResponse(template.render(context, request))

    return response


def send_ticket_email(request):
    email = request.GET.get('email')
    name = request.GET.get('name')
    message = request.GET.get('message')
    subject = request.GET.get('subject')
    helpdesk = os.environ.get('EMAIL_HELPDESK', None)
    if email == None or name == None or message == None or subject == None or helpdesk == None:
        return JsonResponse({'status': 'Missing params'})
    else:
        try:
            send_mail(subject, message, email, [helpdesk], fail_silently=False)
            return JsonResponse({'status': 'sent'})
        except:
            return JsonResponse({'status': 'send_mail fail'})


def disk_thresholds(request):
    cfg = get_config()

    disk_percent_warning = cfg.get('main', 'disk_percent_warning')
    disk_percent_alert = cfg.get('main', 'disk_percent_alert')
    return JsonResponse({
        "disk_percent_warning": disk_percent_warning,
        "disk_percent_alert": disk_percent_alert
    })


@csrf_exempt
def edit_qlf_config(request):
    # TODO: Use configparser
    """Edit qlf.cfg file"""
    body = json.loads(request.body)
    keys = body.get('keys')
    values = body.get('values')
    if keys is not None and values is not None:
        edit_qlf_config_file(keys, values)
        return JsonResponse({
            "keys": keys,
            "values": values
        })
    else:
        return JsonResponse({
            'error': 'Missing key or value'
        })


def default_configuration(request):
    set_default_configuration()
    return JsonResponse({
        'status': 'Done'
    })

def get_camera_log(request):
    process = request.GET.get('process')
    camera = request.GET.get('camera')
    if not process or not camera:
            return JsonResponse({
                'lines': ['missing process or camera']
            })
    job = Job.objects.filter(process=process, camera=camera)
    log = []
    if job:
        log_path = job[0].logname

        cfg = get_config()
        spectro_redux = cfg.get("namespace", "desi_spectro_redux")
        path = '{}/{}'.format(spectro_redux, log_path)
        try:
            arq = open(path, 'r')
            log = arq.readlines()
        except FileNotFoundError:
            log = ['File not found']
    return JsonResponse({
        'lines': log
    })
