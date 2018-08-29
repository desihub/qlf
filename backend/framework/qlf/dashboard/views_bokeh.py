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
from dashboard.bokeh.globalsnr.main import GlobalSnr
from dashboard.bokeh.timeseries.main import TimeSeries
from dashboard.bokeh.regression.main import Regression

from .models import Process

from django.template import loader
from django.http import HttpResponse

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


def get_footprint(request):
    """Generates and render png"""
    template = loader.get_template('dashboard/fits_to_png.html')
    # Generate Footprint
    footprint = Footprint().render()
    context = {'image': footprint}
    response = HttpResponse(template.render(context, request))

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
        elif qa == 'globalsnr':
            qa_html = GlobalSnr(process_id, arm, spectrograph).load_qa()
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
    start = request.GET.get('start')
    end = request.GET.get('end')
    try:
        if plot == 'timeseries':
            series_html = TimeSeries(xaxis, start, end).render()
        elif plot == 'regression':
            series_html = Regression(xaxis, yaxis, start, end).render()
        else:
            series_html = "Couldn't load plot"
    except Exception as err:
        series_html = "Can't load QA: {}".format(err)

    context = {'image': series_html}
    response = HttpResponse(template.render(context, request))

    return response
