import os
import logging
import pandas as pd
import requests
from furl import furl
from bokeh.plotting import Figure

QLF_API_URL = os.environ.get('QLF_API_URL',
                             'http://localhost:8000/dashboard/api')

logger = logging.getLogger(__name__)


def get_data(name, params):
    """
    Returns a panda dataframe so that we can access the QA data arrays
    e.g. data.MEDIAN_SNR

    args:
        name (str): QA file name
        params (list): Metrics to be rescued in QA
    """

    api = requests.get(QLF_API_URL).json()

    qa = requests.get(api['qa'], params={'name': name}).json()
    qa = qa['results']

    metrics = {}

    if not qa:
        logger.warn('{} not found in database'.format(name))
        return pd.DataFrame.from_dict(metrics, orient='index').transpose()

    full_metrics = qa[0]['metrics']

    for metric in params:
        if metric not in full_metrics:
            logger.warn('The {} metric is not present in {}'.format(metric, name))

        metrics[metric] = full_metrics.get(metric, [])

    return pd.DataFrame.from_dict(metrics, orient='index').transpose()


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
        params={'paginate': 'null', 'fields': ','.join(['arm', 'spectrograph'])}
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


def init_xy_plot(hover):
    """
    Defaults for xy plots
    """
    plot = Figure(tools="pan,wheel_zoom,box_zoom,reset,tap")
    plot.add_tools(hover)

    return plot


def get_url_args(curdoc, defaults=None):
    """
    Return url args recovered from django_full_path cookie in
    the bokeh request header.
    If url args are not provided, default values can be used
    instead
    """
    args = {}

    if defaults:
        for key in defaults:
            args[key] = defaults[key]

    http_request = curdoc().session_context.request

    logger.info(http_request)

    if http_request and 'django_full_path' in http_request.cookies:
        uri = http_request.cookies['django_full_path'].value
        tmp = furl(uri).args

        for key in tmp:
            args[key] = tmp[key]

        logger.info('URI: {}'.format(uri))
        logger.info('ARGS: {}'.format(tmp))
        logger.info(__name__)

        # the bokeh app name is the second segment of the url path
        args['bokeh_app'] = furl(uri).path.segments[1]

    return args


def write_info(qa_name, params):
    """
    Writes informations in params as a string to be showed in dashboard"""
    info =""""""
    nlines=0
    dict_test_keys=dict(
        getrms =  ['NOISE_NORMAL_RANGE', 'NOISE_WARN_RANGE'],
        skycont =  ['SKYCONT_NORMAL_RANGE', 'SKYCONT_WARN_RANGE', 'B_CONT', 'R_CONT', 'Z_CONT'],
        xwsigma =  ['B_PEAKS', 'R_PEAKS', 'Z_PEAKS', 'XWSIGMA_NORMAL_RANGE', 'XWSIGMA_WARN_RANGE'],
        skyresid =  ['PCHI_RESID', 'PER_RESID', 'RESID_NORMAL_RANGE', 'RESID_WARN_RANGE', 'BIN_SZ'],
        countbins =  ['CUTHI', 'CUTMED', 'CUTLO', 'NGOODFIB_WARN_RANGE', 'NGOODFIB_NORMAL_RANGE'],
        skypeak =  ['B_PEAKS', 'R_PEAKS', 'Z_PEAKS', 'PEAKCOUNT_NORMAL_RANGE', 'PEAKCOUNT_WARN_RANGE'],
        getbias =  ['BIAS_NORMAL_RANGE',  'BIAS_WARN_RANGE', 'PERCENTILES'],
        countpix =  ['NPIX_NORMAL_RANGE', 'NPIX_WARN_RANGE', 'CUTLO', 'CUTHI'],
        integ =  ['MAGDIFF_WARN_RANGE', 'MAGDIFF_NORMAL_RANGE'],
        snr =  ['FIDSNR_NORMAL_RANGE', 'FIDSNR_WARN_RANGE', 'FIDMAG'])

    keys = dict_test_keys[qa_name]
    for ii in keys:
            info +="""{:>24}: {}\n""".format(ii, params[ii])
            nlines +=1
    return info, nlines

def write_description(qa_name):
    """Descriptions to be displayed in QA plots."""
    info_dic={"getbias":
          ["Bias From Overscan", "Mean of values in overscan covered by each amplifier." ],#"Used to calculate mean and median of region of 2D image, including overscan"],
            "getrms":["Get RMS", "RMS of full region covered by each amplifier."],#"Used to calculate RMS of region of 2D image, including overscan."],
        "countpix": ["Count Pixels", "Number pixels above 'CUTHI' threshold per amplifier." ],#"Count number of pixels above three configured thresholds."],
          #+"Quantities should be independent of exposure length."],
        "xwsigma":["XWSigma","Calculate PSF sigma in spatial and wavelength directions independently using "
          +"configured sky lines."],
        "countbins":["Count Spectral Bins","Count the number of wavelength bins above three configured thresholds."],
        "skycont":["Sky Continuum","Measurement of sky continuum in configured inter-line sky regions on sky fibers."
          #+"There are at least two such regions configured per half-fiber (i.e. In the region covered by each of the " 
          #+"2 amps covering the fiber)."
                  ],
        "skypeak":["Sky Peaks","Measurement of counts in windows around configured peak sky wavelengths on all fibers "
          +"aside from standard star fibers."
                   #  There are at least two such peaks configured per half-fiber" 
          #+"(i.e. In the region covered by each of the 2 amps covering the fiber)."
                  ],
        "skyresid":["Sky Residual", "Median of residuals in each wavelength bin" ],#"Number of wavelength bins above three configured thresholds."],
        "integ":["Integrate Spectrum","Sum of counts for stars fibers"],
          #Number of wavelength bins above three configured thresholds."],
        "snr":["Calculate SNR",  "Signal-to-noise ratio measurements for individual targets."]}
    
    text="""<body><p  style="text-align:left; color:#262626; font-size:20px;">
            <b>{}</b> <br>{}</body>""".format(info_dic[qa_name][0],info_dic[qa_name][1])                  
    return text




if __name__ == '__main__':
    logger.info('Standalone execution...')
