from dashboard.bokeh.fits2png.fits2png import Fits2png
from dashboard.bokeh.qacountpix.main import Countpix
from dashboard.bokeh.qagetbias.main import Bias
from dashboard.bokeh.qagetrms.main import RMS
from dashboard.bokeh.qaxwsigma.main import Xwsigma
from dashboard.bokeh.qacountbins.main import Countbins
from dashboard.bokeh.qaskycont.main import Skycont
from dashboard.bokeh.qaskypeak.main import Skypeak
from dashboard.bokeh.qainteg.main import Integ
from dashboard.bokeh.qasnr.main import SNR
from dashboard.bokeh.qacheckflat.main import Flat
from dashboard.bokeh.qacheckarc.main import Arc
from dashboard.bokeh.qaxyshifts.main import Xyshifts
from dashboard.bokeh.qaskyR.main import SkyR
from dashboard.bokeh.globalfiber.main import GlobalFiber
from dashboard.bokeh.globalfocus.main import GlobalFocus
from dashboard.bokeh.footprint.main import Footprint
from dashboard.bokeh.footprint.object_count import ObjectStatistics
from dashboard.bokeh.globalsnr.main import GlobalSnr
from dashboard.bokeh.timeseries.main import TimeSeries
from dashboard.bokeh.regression.main import Regression
from dashboard.bokeh.spectra.main import Spectra
from datetime import datetime, timedelta

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

def filter_processed_exposures(begin_date, end_date, program):
    if not program or program == 'all':
        exposures_radec = Process.objects.all().values('exposure__telra', 'exposure__teldec').distinct()
    else:
        begin_date = datetime.strptime(begin_date, "%Y%m%d")
        end_date = datetime.strptime(end_date, "%Y%m%d") + timedelta(days=1)
        exposures_radec = Process.objects.filter(
            exposure__program=program).filter(exposure__dateobs__gte=begin_date).filter(exposure__dateobs__lte=end_date).values('exposure__telra', 'exposure__teldec').distinct()

    return exposures_radec

def get_footprint(request):
    """Generates and render png"""
    template = loader.get_template('dashboard/fits_to_png.html')
    start = request.GET.get('start')
    end = request.GET.get('end')
    program = request.GET.get('program')
    if not program:
        processed_exposures = []
    elif not start or not end:
        context = {'image': "Select start and end date"}
        response = HttpResponse(template.render(context, request))

        return response
    else:
        processed_exposures = filter_processed_exposures(start, end, program)

    # Generate Footprint
    footprint = Footprint().render(processed_exposures)
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

    total_obj = [0]*2
    good = [0]*2
    bad = [0]*2

    for ids in process_ids:
        nobj, snr, fiber = ObjectStatistics(ids).generate_statistics()

        for i, o in enumerate(['TGT', 'STAR']):
            good[i] += snr['NORMAL'][o] + snr['WARN'][o]
            bad[i] += snr['ALARM'][o]
            total_obj[i] = str(int(good[i])+int(bad[i]))
            # good[i] += snr['NORMAL'][o] + snr['WARN'][o] + fiber['GOOD'][o]
            # bad[i] += snr['ALARM'][o] + fiber['BAD'][o]

    result = dict(objects=['TGT', 'STAR'],
                  total=total_obj,
                  good=[int(good[i]) for i in range(2)],
                  bad=[int(bad[i]) for i in range(2)])

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
            qa_html = Flat(process_id, arm,spectrograph).load_qa() #'No Drill Down'
        elif qa == 'qacheckarc':
            qa_html = Arc(process_id, arm,spectrograph).load_qa() #'No Drill Down'
        elif qa == 'qaxyshifts':
            qa_html = Xyshifts(process_id, arm,spectrograph).load_qa()
        elif qa == 'qaskyrband':
            qa_html = SkyR(process_id, arm,spectrograph).load_qa()
        else:
            qa_html = "Couldn't load QA"
    except Exception as err:
        qa_html = "Can't load QA: {}".format(err)

    context = {'image': qa_html}
    response = HttpResponse(template.render(context, request))

    return response

def load_spectra(request):
    template = loader.get_template('dashboard/spectra.html')
    # Generate Image
    spectra = request.GET.get('spectra')
    spectrograph = request.GET.get('spectrograph')
    process_id = request.GET.get('process_id')
    arm = request.GET.get('arm')
    fiber = request.GET.get('fiber')
    if arm == 'all':
        arms=['b', 'r', 'z']
    else:
        arms=[arm]
    try:
        if spectra == 'spectra':
            spectra_html = Spectra(process_id, arms).load_spectra()
        elif spectra == 'spectra_fib':
            spectra_html = Spectra(process_id, arms).render_spectra(
                fiber, spectrograph)
    except Exception as err:
        spectra_html = "Can't load spectra: {}".format(err)

    context = {'image': spectra_html}
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
            series_html = Regression(xaxis, yaxis, start, end, camera).render()
        else:
            series_html = "Couldn't load plot"
    except Exception as err:
        series_html = "Can't load QA: {}".format(err)

    context = {'image': series_html}
    response = HttpResponse(template.render(context, request))

    return response
