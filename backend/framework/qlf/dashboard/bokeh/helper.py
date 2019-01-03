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


def get_last_process():
    """
    Returns last process
    """

    api = requests.get(QLF_API_URL).json()
    return requests.get(api['last_process']).json()


def get_merged_qa_scalar_metrics(process_id, cam):
    """
    Returns cam scalar metrics
    """

    return QLFModels().get_output(process_id, cam)


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

    info_dic ={ 'countbins': ["Count Spectral Bins", 'Number of fibers with a nonzero number of bins above highest threshold'],
                'skycont': ["Sky Continuum", 'Sky continuum in all configured continuum areas averaged over all sky fibers'],
                'countpix': ["Count Pixels", 'Fraction of the pixels per amp that are above CUTPIX = 5 sigmas '],
                'skypeak': ["Sky Peaks", 'Sky continuum in all configured continuum areas averaged over all sky fibers'],
                'getbias': ["Bias From Overscan", 'Value of bias averaged over each amplifier'],
                'getrms': ["Get RMS", 'Value of RMS for each amplifier read directly from the header of the pre processed image'],
                'snr': ["Calculate SNR", 'List of average signal to noise ratio (SNR) for the N target type'],
                'integ': ["Integrate Spectrum", 'List of the average fiber magnitude for each of N target types in this camera'],
                'xwsigma': ["XWSigma", 'Fitted X and W SIGMA averaged over isolated bright sky wavelengths'],
                'checkHDUs': ['',''],
                'fiberflat':["Check Fiber Flat", "The average wavelength in the fiberflat frame"],
                'arc':["Check ARC", """Number of fibers for which the first, second and third Legendre polynomial (P0, P1 and P2) in their""" \
                        +""" best-fit are outside 2 sigmas from the median of each"""],#"Number of fibers with Wsigma fit parameters (P0, P1, and P2) outside of 2 times RMS around medians"],
                'xyshifts': ["XYSHIFTS","List of two averaged values (in pixel unit) for the fiber traces in X, Y directions"],
                'skyR': ["SKYRBAND","Average value of sky background in R-band"],
                'hdu':["CHECK_HDU", ]
              }
    
    text="""<body><p  style="text-align:left; color:#262626; font-size:1.5vw;">
            <b>{}</b> <br>{}</body>""".format(info_dic[qa_name][0],info_dic[qa_name][1])
    return text


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
