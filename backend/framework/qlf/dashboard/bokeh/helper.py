import os
import logging
import requests
from furl import furl
from bokeh.plotting import Figure
from dashboard.models import Process, Job
from qlf_models import QLFModels
import sys

QLF_API_URL = os.environ.get('QLF_API_URL',
                             'http://localhost:8000/dashboard/api')

logger = logging.getLogger(__name__)


def get_arms_and_spectrographs():
    """
    Rescues all the arms and spectrographs.

    return: {"arms": [...], "spectrographs": [...]}
    """
    arms = list()
    spectrographs = list()

    api = requests.get(QLF_API_URL).json()

    cameras = requests.get(
        api['camera'],
        params={'paginate': 'null', 'fields': ','.join(
            ['arm', 'spectrograph'])}
    ).json()

    for camera in cameras:
        arms.append(camera['arm'])
        spectrographs.append(camera['spectrograph'])

    return {"arms": list(set(arms)), "spectrographs": list(set(spectrographs))}


def get_last_process():
    """
    Returns last process
    """

    api = requests.get(QLF_API_URL).json()
    return requests.get(api['last_process']).json()


def get_exposure_ids():
    """
    Returns the list with exposure ids
    """

    api = requests.get(QLF_API_URL).json()

    r = requests.get(
        api['exposure'], params={'paginate': 'null', 'fields': 'exposure_id'}
    ).json()

    return [int(e['exposure_id']) for e in r]


def get_exposures():
    """
    Returns the list of registered exposures
    """

    api = requests.get(QLF_API_URL).json()

    # TODO: filter exposures by flavor?
    r = requests.get(
        api['exposure'],
        params={
            'paginate': 'null',
            'fields': ','.join(['exposure_id', 'flavor', 'telra', 'teldec'])
        }
    ).json()

    expid = [int(e['exposure_id']) for e in r]
    flavor = [e['flavor'] for e in r]
    ra = [e['telra'] for e in r]
    dec = [e['teldec'] for e in r]

    return {
        'expid': expid, 'flavor': flavor,
        'ra': ra, 'dec': dec
    }


def get_cameras():
    """
    Returns the list of registered cameras
    """

    api = requests.get(QLF_API_URL).json()

    return requests.get(api['camera'], params={'paginate': 'null'}).json()


def get_merged_qa_scalar_metrics(process_id, cam):
    """
    Returns cam scalar metrics
    """

    # scalar_metrics = dict()
    # try:
    #     obj = Job.objects.filter(process_id=process_id).get(camera=cam)
    #     scalar_metrics = obj.output
    # except Job.DoesNotExist:
    #     scalar_metrics = None
    # return scalar_metrics
    return QLFModels().get_output(process_id, cam)


def load_fits(process_id, cam):
    '''Load reduced fits '''
    from astropy.io import fits

    try:
        process = Process.objects.get(pk=process_id)
        exposure = process.exposure
        folder = "/app/spectro/redux/exposures/{}/{:08d}".format(
            exposure.night, process.exposure_id)

        file = "sframe-{}-{:08d}.fits".format(cam, process.exposure_id)
        fitsfile = fits.open('{}/{}'.format(folder, file))
        return fitsfile

    except Exception as err:
        logger.info('{}'.format(err))
        return None


def init_xy_plot(hover, yscale):
    """
    Defaults for xy plots
    """
    plot = Figure(tools=[hover, "pan,wheel_zoom,box_zoom,reset,tap"],active_drag="box_zoom",
                  y_axis_type=yscale, plot_width=601, plot_height=400)
    # plot.add_tools(hover)

    return plot


def write_info(qa_name, params):
    """
    Writes informations in params as a string to be showed in dashboard"""
    info = """"""
    nlines = 0
    dict_test_keys = dict(
        getrms=['NOISE_AMP_NORMAL_RANGE', 'NOISE_AMP_WARN_RANGE'],
        skycont=['SKYCONT_NORMAL_RANGE', 'SKYCONT_WARN_RANGE',
                 'B_CONT', 'R_CONT', 'Z_CONT'],
        xwsigma=['B_PEAKS', 'R_PEAKS', 'Z_PEAKS',
                 'XWSIGMA_NORMAL_RANGE', 'XWSIGMA_WARN_RANGE'],
        skyresid=['PCHI_RESID', 'PER_RESID',
                  'MED_RESID_NORMAL_RANGE', 'MED_RESID_WARN_RANGE', 'BIN_SZ'],
        countbins=['CUTHI', 'CUTMED', 'CUTLO',
                   'NGOODFIB_WARN_RANGE', 'NGOODFIB_NORMAL_RANGE'],
        skypeak=['B_PEAKS', 'R_PEAKS', 'Z_PEAKS',
                 'PEAKCOUNT_NORMAL_RANGE', 'PEAKCOUNT_WARN_RANGE'],
        # , 'PERCENTILES'],
        getbias=['BIAS_AMP_NORMAL_RANGE',  'BIAS_AMP_WARN_RANGE'],
        countpix=['LITFRAC_AMP_NORMAL_RANGE',
                  'LITFRAC_AMP_WARN_RANGE', 'CUTPIX'],  # , 'LITFRAC_AMP_REF'
        integ=['DELTAMAG_WARN_RANGE', 'DELTAMAG_NORMAL_RANGE'],
        snr=['FIDSNR_TGT_NORMAL_RANGE', 'FIDSNR_TGT_WARN_RANGE', 'FIDMAG'])

    keys = dict_test_keys[qa_name]
    for ii in keys:
        info += """{:>24}: {}\n""".format(ii, params[ii])
        nlines += 1
    return info, nlines


def write_description(qa_name):
    """Descriptions to be displayed in QA plots."""

    info_dic2 = {'countbins': ["Count Spectral Bins", "Number of bins above a threshold per spectrum."],
                 'skycont': ["Sky Continuum", "Mean sky continuum after fiber flattening"],
                 'countpix': ["Count Pixels", "Fraction of pixels lit after pre processing"],
                 'skypeak': ["Sky Peaks",
                             "This QA for QuickLook includes the calculation of the counts and RMS at peak sky wavelengths in a 1D spectrum."],  # "Count for Sky Fiber after ApplyFiberFlat QL"],
                 'getbias': ["Bias From Overscan", "Bias from overscan region after pre processing"],
                 'skyresid': ["Sky Residual", "Randomly Selected sky substracted, fiber flattened spectra"],
                 'getrms': ["Get RMS", " NOISE image counts per amplifier"],
                 'snr': ["Calculate SNR", "Signal-to-Noise ratio after sky substraction"],
                 # Total integrals of STD spectra SkySub QL"
                 'integ': ["Integrate Spectrum", "Integral counts for standard stars"],
                 'xwsigma': ["XWSigma", "X & W sigma over sky peaks"],
                 'checkHDUs': ['', '']}

    info_dic = {'countbins': ["Count Spectral Bins", "Number of bins above a threshold per spectrum."],
                'skycont': ["Sky Continuum", "Mean sky continuum after fiber flattening"],
                'countpix': ["Count Pixels", "Fraction of pixels lit after pre processing"],
                # "Count for Sky Fiber after ApplyFiberFlat QL"],
                'skypeak': ["Sky Peaks", "Sky level at peak sky wavelengths in a 1D spectrum"],
                'getbias': ["Bias From Overscan", "Bias from overscan region after pre processing"],
                'skyresid': ["Sky Residual", "Randomly Selected sky substracted, fiber flattened spectra"],
                'getrms': ["Get RMS", " NOISE image counts per amplifier"],
                'snr': ["Calculate SNR", "Signal-to-Noise ratio after sky substraction"],
                # Total integrals of STD spectra SkySub QL"
                'integ': ["Integrate Spectrum", "Integral counts for standard stars"],
                'xwsigma': ["XWSigma", "X & W sigma over sky peaks"],
                'checkHDUs': ['', '']}

    text = """<body><p  style="text-align:left; color:#262626; font-size:20px;">
            <b>{}</b> <br>{}</body>""".format(info_dic[qa_name][0], info_dic[qa_name][1])
    return text


def eval_histpar(yscale, hist):
    """ Common parameters for histograms"""
    from numpy import log10
    if yscale == 'log':
        ylabel = "Frequency + 1"
        yrange = (1, 1. * 10**(int(log10(max(hist))) + 1))
        bottomval = 'bottomplusone'
        histval = 'histplusone'
    else:
        ylabel = "Frequency"
        yrange = (-0.1*max(hist), 1.1*max(hist))
        bottomval = 'bottom'
        histval = 'hist'
    return [ylabel, yrange, bottomval, histval]


def get_palette(name_of_mpl_palette):
    """ Transforms a matplotlib palettes into a bokeh 
    palettes
    """
    import numpy as np
    from matplotlib.colors import rgb2hex
    import matplotlib.cm as cm
    # choose any matplotlib colormap here
    colormap = cm.get_cmap(name_of_mpl_palette)
    bokehpalette = [rgb2hex(m) for m in colormap(np.arange(colormap.N))]
    return bokehpalette


if __name__ == '__main__':
    logger.info('Standalone execution...')
