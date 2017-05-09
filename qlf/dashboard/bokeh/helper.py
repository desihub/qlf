import os
import pandas as pd
import requests
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
    r = list()
    api = requests.get(QLF_API_URL).json()
    data = requests.get(api['camera']).json()['results']
    for i in data:
        if i['exposure'] == expid:
            r.append(i)
    return r

def get_all_exposure():
    api = requests.get(QLF_API_URL).json()
    data = requests.get(api['exposure']).json()['results']
    return data

def get_all_camera():
    api = requests.get(QLF_API_URL).json()
    data = requests.get(api['camera']).json()['results']
    return data

def get_all_qa():
    api = requests.get(QLF_API_URL).json()
    data = requests.get(api['qa']).json()['results']
    return data


def get_exposure_info():
    """
    Returns the list of registered exposures
    """

    api = requests.get(QLF_API_URL).json()

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


if __name__ == '__main__':

    data = get_data()
    print(data.info())
