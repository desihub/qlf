import logging
import configparser
import os
import shutil

logger = logging.getLogger()

qlf_root = os.getenv('QLF_ROOT')

if not qlf_root:
    raise ValueError('QLF_ROOT not define.')


def get_config(config_path=None):
    """ """

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
    desi_spectro_data = os.path.normpath(cfg.get(
        "namespace",
        "desi_spectro_data"
        )
    )

    delete_files(os.path.join(
        desi_spectro_redux,
        'exposures',
    ))

    delete_files(os.path.join(
        desi_spectro_data,
    ))

    delete_files(os.path.join(
        desi_spectro_redux,
        'calib2d',
    ))

    delete_files(os.path.join(
        desi_spectro_redux,
        'calib2d',
        'psf',
    ))


def delete_files(path):
    for night in os.listdir(path):
        if night != '20190101' and night != 'psf':
            night_path = os.path.join(path, night)
            if os.path.exists(night_path):
                shutil.rmtree(night_path)
