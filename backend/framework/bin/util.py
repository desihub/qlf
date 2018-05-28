import logging
import configparser
import os
import shutil

logger = logging.getLogger()

qlf_root = os.getenv('QLF_ROOT')

if not qlf_root:
    raise ValueError('QLF_ROOT not define.')


def get_config(config_path=None):
    """ Gets config """

    if not config_path:
        config_path = os.path.join(
            qlf_root,
            "framework/config/qlf.cfg"
        )

    cfg = configparser.ConfigParser()
    cfg.read(config_path)

    section = 'environment'

    if not cfg.has_section(section):
        cfg.add_section(section)

    cfg.set(section, 'qlf_root', qlf_root)

    return cfg


def delete_exposures():
    cfg = get_config()

    desi_spectro_redux = cfg.get('namespace', 'desi_spectro_redux')
    desi_spectro_data = cfg.get('namespace', 'desi_spectro_data')

    delete_files(desi_spectro_redux)
    delete_files(desi_spectro_data)


def delete_files(path):
    for directory in os.listdir(path):
        _path = os.path.join(path, directory)
        if os.path.isdir(_path):
            shutil.rmtree(_path)
