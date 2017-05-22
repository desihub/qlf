import os
import pandas as pd
import requests
from furl import furl
from bokeh.plotting import Figure

QLF_API_URL = os.environ.get('QLF_API_URL',
                             'http://localhost:8000/dashboard/api')


def get_data(name=None):
    """
    Returns a panda dataframe so that we can access the QA data arrays for each expid,
    e.g. data.loc[expid].MEDIAN_SNR
    """
    api = requests.get(QLF_API_URL).json()

    r = requests.get(api['qa'], params={'name': name}).json()

    data = None

    if len(r['results']) > 0:
        value = eval(r['results'][0]['value'])
        data = pd.DataFrame.from_dict(value, orient='index').transpose()

    return data

def get_camera_by_exposure(expid):
    processesList = list()
    cameraList = list()
    cameraReturn = list()
    api = requests.get(QLF_API_URL).json()
    processes = requests.get(api['process']).json()

    for process in processes:
        if process['exposure'] == expid:
            for process_job in process['jobs']:
                processesList.append(process_job['process'])
    jobs = requests.get(api['job']).json()
    for job in jobs:
        if job['process'] in processesList:
            cameraList.append(job['camera'])
    cameras = requests.get(api['camera']).json()
    for camera in cameras:
        if camera['camera'] in cameraList:
            cameraReturn.append(camera)
    return cameraReturn

def get_all_exposure():
    api = requests.get(QLF_API_URL).json()
    data = requests.get(api['exposure']).json()
    return data

def get_all_camera():
    api = requests.get(QLF_API_URL).json()
    data = requests.get(api['camera']).json()
    return data

def get_all_qa():
    api = requests.get(QLF_API_URL).json()
    data = requests.get(api['qa']).json()
    return data

def get_last_process():
    """
    Returns last process 
    """

    api = requests.get(QLF_API_URL).json()
    data = requests.get(api['monitor']).json()
    if data:
        return data
    else:
        return None

def get_exposure_info():
    """
    Returns the list of registered exposures
    """

    api = requests.get(QLF_API_URL).json()
    data = requests.get(api['qa']).json()['results']

    # TODO: filter exposures by flavor?
    r = requests.get(api['exposure']).json()
    expid = [int(e['expid']) for e in r['results']]
    flavor = [e['flavor'] for e in r['results']]

    return {'expid': expid, 'flavor': flavor}


def get_camera_info():
    """
    Returns the list of registered cameras
    """

    api = requests.get(QLF_API_URL).json()

    r = requests.get(api['camera']).json()

    camera = [c['camera'] for c in r['results']]
    arm = [c['arm'] for c in r['results']]
    spectrograph = [c['spectrograph'] for c in r['results']]

    return {'camera': camera, 'arm': arm, 'spectrograph': spectrograph}


def init_xy_plot(hover):
    """
    Defaults for xy plots
    """
    plot = Figure(tools="pan,wheel_zoom,box_zoom,reset")
    plot.add_tools(hover)

    return plot


def get_url_args(curdoc, defaults=None):
    """Return url args recovered from django_full_path cookie in
    the bokeh request header.
    If url args are not provided, default values can be used
    instead
    """
    args = {}
    if defaults:
        for key in defaults:
            args[key] = defaults[key]

    r = curdoc().session_context.request

    if r:
        if 'django_full_path' in r.cookies:
            django_full_path = r.cookies['django_full_path'].value
            tmp = furl(django_full_path).args
            for key in tmp:
                args[key] = tmp[key]

            # the bokeh app name is the second segment of the url path
            args['bokeh_app'] = furl(django_full_path).path.segments[1]

    return args



if __name__ == '__main__':

    data = get_data()
    print(data.info())
