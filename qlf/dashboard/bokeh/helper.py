import os
import logging
import pandas as pd
import requests
from furl import furl
import ast
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

    logger.info('QA: {}'.format(qa))

    metrics = {}

    if not qa:
        logger.warn('{} not found in database'.format(name))
        return pd.DataFrame.from_dict(metrics, orient='index').transpose()

    full_metrics = qa[0]['metric'].replace('inf', '0')
    full_metrics = ast.literal_eval(full_metrics)

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

        # the bokeh app name is the second segment of the url path
        args['bokeh_app'] = furl(uri).path.segments[1]

    return args


if __name__ == '__main__':
    logger.info('Standalone execution...')
