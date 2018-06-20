from util import get_config
import os
import shutil


def delete_raw():
    cfg = get_config()
    desi_spectro_data = cfg.get('namespace', 'desi_spectro_data')
    delete_files(desi_spectro_data)


def delete_reduced():
    cfg = get_config()
    desi_spectro_redux = cfg.get('namespace', 'desi_spectro_redux')
    delete_files(desi_spectro_redux)


def delete_logs():
    cfg = get_config()
    logfile = cfg.get('main', 'logfile')
    logpipeline = cfg.get('main', 'logpipeline')
    with open(logfile, 'w'):
        pass
    with open(logpipeline, 'w'):
        pass


def delete_files(path):
    for directory in os.listdir(path):
        _path = os.path.join(path, directory)
        if os.path.isdir(_path):
            shutil.rmtree(_path)
