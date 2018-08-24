import os
import shutil


def delete_raw():
    desi_spectro_redux = os.environ.get('DESI_SPECTRO_DATA')
    delete_files(desi_spectro_data)


def delete_reduced():
    desi_spectro_redux = os.environ.get('DESI_SPECTRO_REDUX')
    delete_files(desi_spectro_redux)


def delete_logs():
    logfile = os.path.join(qlf_root, "logs", "qlf.log")
    logpipeline = os.path.join(qlf_root, "logs", "pipeline.log")
    with open(logfile, 'w'):
        pass
    with open(logpipeline, 'w'):
        pass


def delete_files(path):
    for directory in os.listdir(path):
        _path = os.path.join(path, directory)
        if os.path.isdir(_path):
            shutil.rmtree(_path)
