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
from dashboard.bokeh.footprint.main import Footprint
from dashboard.bokeh.footprint.object_count import ObjectStatistics
from dashboard.bokeh.globalsnr.main import GlobalSnr
from dashboard.bokeh.timeseries.main import TimeSeries
from dashboard.bokeh.regression.main import Regression
import datetime

from .models import Process, Exposure

from django.template import loader
from django.http import HttpResponse
from django.http import JsonResponse
from astropy.io import fits

import os

spectro_data = os.environ.get('DESI_SPECTRO_DATA')


from log import get_logger
import os

qlf_root = os.environ.get('QLF_ROOT')

logger = get_logger(
    "qlf.bokeh",
    os.path.join(qlf_root, "logs", "bokeh.log")
)

def embed_bokeh(request, bokeh_app):
    """Render the requested app from the bokeh server"""

    # http://bokeh.pydata.org/en/0.12.5/docs/reference/embed.html

    # TODO: test if bokeh server is reachable

    bokeh_script = server_document(arguments=request.GET, url="{}/{}".format(settings.QLF_BASE_URL,
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


def filter_processed_exposures(start, end, program):
    start_date = datetime.datetime.strptime(start, "%Y%m%d").replace(
        tzinfo=datetime.timezone.utc)
    end_date = datetime.datetime.strptime(end, "%Y%m%d").replace(
        tzinfo=datetime.timezone.utc) + datetime.timedelta(days=1)

    if not program or program == 'all':
        exposures = Exposure.objects.filter(
            dateobs__gte=start_date, dateobs__lte=end_date)
    else:
        exposures = Exposure.objects.filter(
            program=program, dateobs__gte=start_date, dateobs__lte=end_date)

    processed_exposures = list()
    for exposure in exposures:
        if list(Process.objects.filter(exposure_id=exposure.pk)) != []:
            processed_exposures.append(exposure)

    return processed_exposures

def get_footprint(request):
    """Generates and render png"""
    template = loader.get_template('dashboard/fits_to_png.html')
    start = request.GET.get('start')
    end = request.GET.get('end')
    program = request.GET.get('program')
    if not program:
        exposures_radec = {"ra": [], "dec": []}
    elif not start or not end:
        context = {'image': "Select start and end date"}
        response = HttpResponse(template.render(context, request))

        return response
    else:
        processed_exposures = filter_processed_exposures(start, end, program)

        exposures_ra = list()
        exposures_dec = list()
        for exposure in processed_exposures:
            if exposure.telra:
                exposures_ra.append(exposure.telra)
            if exposure.teldec:
                exposures_dec.append(exposure.teldec)

        exposures_radec = {"ra": exposures_ra, "dec": exposures_dec}
    # Generate Footprint
    footprint = Footprint().render(exposures_radec)
    context = {'image': footprint}
    response = HttpResponse(template.render(context, request))

    return response


def footprint_object_type_count(request):
    """Generates exposures object type count"""
    start = request.GET.get('start')
    end = request.GET.get('end')
    program = request.GET.get('program')
    processed_exposures = filter_processed_exposures(start, end, program)
    process_ids = []
    for exposure in processed_exposures:
        if list(Process.objects.filter(exposure_id=exposure.pk)) != []:
            process_ids.append(Process.objects.filter(exposure_id=exposure.pk).last().pk)
            
    total_obj = [0]*4
    snr_good = [0]*4
    fib_good = [0]*4
    snr_bad = [0]*4
    fib_bad = [0]*4

    good = [0]*4
    bad = [0]*4

    for ids in process_ids:
        nobj, snr, fiber = ObjectStatistics(ids).generate_statistics()

        for i, o in enumerate(['TGT', 'STAR']):
            total_obj[i] += nobj[o]
            good[i] += snr['NORMAL'][o] + snr['WARN'][o] + fiber['GOOD'][o]
            bad[i] += snr['ALARM'][o] + fiber['BAD'][o]

    result = dict(objects=['TGT', 'STAR'],
                  total=total_obj,
                  good=[int(good[i]) for i in range(4)],
                  bad=[int(bad[i]) for i in range(4)])

    return JsonResponse(result)


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
    """Generates and render qas"""
    template = loader.get_template('dashboard/qa.html')
    # Generate Image
    qa = request.GET.get('qa')
    spectrograph = request.GET.get('spectrograph')
    process_id = request.GET.get('process_id')
    arm = request.GET.get('arm')
    try:
        if qa == 'qacountpix':
            qa_html = Countpix(process_id, arm, spectrograph).load_qa()
        elif qa == 'qabias':
            qa_html = Bias(process_id, arm, spectrograph).load_qa()
        elif qa == 'qarms':
            qa_html = RMS(process_id, arm, spectrograph).load_qa()
        elif qa == 'qaxwsigma':
            qa_html = Xwsigma(process_id, arm, spectrograph).load_qa()
        elif qa == 'qacountbins':
            qa_html = Countbins(process_id, arm, spectrograph).load_qa()
        elif qa == 'qaskycont':
            qa_html = Skycont(process_id, arm, spectrograph).load_qa()
        elif qa == 'qapeakcount':
            qa_html = Skypeak(process_id, arm, spectrograph).load_qa()
        elif qa == 'qainteg':
            qa_html = Integ(process_id, arm, spectrograph).load_qa()
        elif qa == 'qaskyresid':
            qa_html = Skyresid(process_id, arm, spectrograph).load_qa()
        elif qa == 'qasnr':
            qa_html = SNR(process_id, arm, spectrograph).load_qa()
        elif qa == 'globalfiber':
            qa_html = GlobalFiber(process_id, arm).load_qa()
        elif qa == 'globalfocus':
            qa_html = GlobalFocus(process_id, arm).load_qa()
        elif qa == 'globalsnr':
            qa_html = GlobalSnr(process_id, arm).load_qa()
        elif qa == 'qahdu':
            qa_html = 'No Drill Down'
        elif qa == 'qacheckflat':
            qa_html = 'No Drill Down'
        elif qa == 'qacheckarc':
            qa_html = 'No Drill Down'
        elif qa == 'qaxyshifts':
            qa_html = 'No Drill Down'
        elif qa == 'qaskyrband':
            qa_html = 'No Drill Down'
        else:
            qa_html = "Couldn't load QA"
    except Exception as err:
        qa_html = "Can't load QA: {}".format(err)

    context = {'image': qa_html}
    response = HttpResponse(template.render(context, request))

    return response


def load_series(request):
    """Generates and render series"""
    template = loader.get_template('dashboard/series.html')
    # Generate Image
    plot = request.GET.get('plot')
    xaxis = request.GET.get('xaxis')
    yaxis = request.GET.get('yaxis')
    camera = request.GET.get('camera')
    start = request.GET.get('start')
    end = request.GET.get('end')
    amp = request.GET.get('amp')

    try:
        if plot == 'timeseries':
            series_html = TimeSeries(yaxis, start, end, camera, amp).render()
        elif plot == 'regression':
            series_html = Regression(xaxis, yaxis, start, end).render()
        else:
            series_html = "Couldn't load plot"
    except Exception as err:
        series_html = "Can't load QA: {}".format(err)

    context = {'image': series_html}
    response = HttpResponse(template.render(context, request))

    return response
