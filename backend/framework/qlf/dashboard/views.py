from rest_framework import (
    authentication, permissions, viewsets, filters,
    status, views
)
import json
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination

from django.db.models import Max, Min

from .models import Job, Exposure, Camera, Process, Configuration, ProcessComment, Fibermap, Product
from .serializers import (
    JobSerializer, ExposureSerializer, CameraSerializer,
    ProcessSerializer, ConfigurationSerializer,
    ProcessJobsSerializer, ProcessingHistorySerializer,
    ObservingHistorySerializer, ExposuresDateRangeSerializer,
    ExposureFlavorSerializer, ProcessCommentSerializer,
    ExposureNightSerializer, FibermapSerializer,
    ProductSerializer
)

from datetime import datetime, timedelta

from django.http import JsonResponse

from .filters import ProcessingHistoryFilter

from django.core.mail import send_mail
import os

from clients import get_exposure_monitoring

import logging

qlf = get_exposure_monitoring()

logger = logging.getLogger(__name__)


class LargeLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 100
    max_limit = 500


class StandartLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 50
    max_limit = 10000


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


class ProductViewSet(DynamicFieldsMixin, DefaultsMixin, viewsets.ModelViewSet):
    """API endpoint for listing Products"""

    queryset = Product.objects.order_by('pk')
    serializer_class = ProductSerializer
    filter_fields = ('key', 'mjd',)


class ProcessViewSet(DynamicFieldsMixin, DefaultsMixin, viewsets.ModelViewSet):
    """API endpoint for listing processes"""

    queryset = Process.objects.order_by('start')
    serializer_class = ProcessSerializer
    filter_fields = ('exposure',)


class QlConfigViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Configuration.objects.order_by('creation_date')
    serializer_class = ConfigurationSerializer
    def list(self, request, *args, **kwargs):
        response = super(QlConfigViewSet, self).list(
            request, args, kwargs)
        try:
            ql_type = request.GET.get('type')
            ql_path = '{}/qlconfig_{}.yaml'.format(os.environ.get('QL_CONFIG_DIR'), ql_type)
            with open(ql_path) as f:
                qlconfig = f.read()
        except Exception as err:
            logger.info(err)
            qlconfig = 'Error reading qlconfig: {}'.format(err)
        response.data = qlconfig
        return response


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
        qlf_root = os.environ.get('QLF_ROOT')
        configuration = dict(
            logfile=os.path.join(qlf_root, "logs", "qlf.log"),
            loglevel=os.environ.get('PIPELINE_LOGLEVEL'),
            logpipeline=os.path.join(qlf_root, "logs", "pipeline.log"),
            arms=os.environ.get('PIPELINE_ARMS'),
            spectrographs=os.environ.get('PIPELINE_SPECTROGRAPHS'),
            desi_spectro_data=os.environ.get('DESI_SPECTRO_DATA'),
            desi_spectro_redux=os.environ.get('DESI_SPECTRO_REDUX'),
            calibration_path=os.environ.get('DESI_CCD_CALIBRATION_DATA'),
            max_workers=os.environ.get('PIPELINE_MAX_WORKERS')
        )
        response.data = {'results': configuration}
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


class ExposureViewSet(DynamicFieldsMixin, DefaultsMixin, viewsets.ModelViewSet):
    """API endpoint for listing exposures"""

    queryset = Exposure.objects.order_by('exposure_id')
    serializer_class = ExposureSerializer
    filter_fields = ('exposure_id',)


class FibermapViewSet(DynamicFieldsMixin, DefaultsMixin, viewsets.ModelViewSet):
    """API endpoint for listing fibermaps"""

    queryset = Fibermap.objects.all()
    serializer_class = FibermapSerializer


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
    disk_percent_warning = os.environ.get('DISK_SPACE_PERCENT_WARNING')
    disk_percent_alert = os.environ.get('DISK_SPACE_PERCENT_ALERT')
    return JsonResponse({
        "disk_percent_warning": disk_percent_warning,
        "disk_percent_alert": disk_percent_alert
    })

def check_ccds(process_dir, camera):
    desi_spectro_data = os.environ.get('DESI_SPECTRO_DATA')
    desi_spectro_redux = os.environ.get('DESI_SPECTRO_REDUX')
    data_path = '{}/{}/desi-{}.fits.fz'.format(desi_spectro_data,
                                            process_dir,
                                            process_dir.split('/')[-1])
    redux_path = '{}/{}/sframe-{}-{}.fits'.format(
                desi_spectro_redux, process_dir, camera, process_dir.split('/')[-1])

    return os.path.exists(data_path) or os.path.exists(redux_path)

def check_spectra(process_dir, camera):
    desi_spectro_redux = os.environ.get('DESI_SPECTRO_REDUX')
    frame_path = "{}/{}/sframe-{}-{}.fits""".format(
        desi_spectro_redux,
        process_dir,
        camera,
        process_dir.split('/')[-1],
    )

    return os.path.exists(frame_path)
    
def check_view_files(request):
    process_id = request.GET.get('process_id')
    p=Process.objects.filter(id=process_id).last()

    exp_zfill = str(p.exposure_id).zfill(8)
    process_dir = p.process_dir
    spectra = False
    ccd = False

    for job in p.process_jobs.all():
        arm = job.camera.arm
        spectrograph = job.camera.spectrograph
        camera = str(arm+spectrograph)
        if check_ccds(process_dir, camera):
            ccd = True

        if check_spectra(process_dir, camera):
            spectra=True

    return JsonResponse({
        "spectra": spectra,
        "ccd": ccd
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

        spectro_redux = os.environ.get('DESI_SPECTRO_REDUX')
        path = '{}/{}'.format(spectro_redux, log_path)
        try:
            arq = open(path, 'r')
            log = arq.readlines()
        except FileNotFoundError:
            log = ['File not found']
    return JsonResponse({
        'lines': log
    })
