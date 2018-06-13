import logging
import configparser
import os
import shutil
import astropy.io.fits
import datetime

logger = logging.getLogger()

qlf_root = os.getenv('QLF_ROOT')

if not qlf_root:
    raise ValueError('QLF_ROOT not define.')

# TODO: flat program can also use flat_preproc.
program_mapping = {
    'flat': 'flat',  # flat_preproc
    'arc': 'arcs',
    'dark': 'darksurvey',
    'gray': 'greysurvey',
    'grey': 'greysurvey',
    'bright': 'brightsurvey'
}


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

def change_config_file(config_file):
    with open(config_file, 'r') as file:
        config = file.readlines()

    for i, line in enumerate(config):
        if 'PSFExpid:' in line:
            config[i] = 'PSFExpid: 0\n'
        elif 'FiberflatExpid:' in line:
            config[i] = 'FiberflatExpid: 1\n'

    cfg = get_config()
    desi_spectro_redux = cfg.get('namespace', 'desi_spectro_redux')
    current_config = '{}/current_config.yaml'.format(desi_spectro_redux)
    with open(current_config, 'w') as file:
        file.writelines(config)
    return current_config

def extract_exposure_data(exposure_id, night):
    """ Extracts exposure data from fits file.

    Arguments:
        exposure_id {int} -- exposure ID
        night {str} -- night (format: YYYYMMDD)

    Returns:
        dict -- exposure data from fits file.
    """

    cfg = get_config()
    desi_spectro_data = cfg.get('namespace', 'desi_spectro_data')
    desi_spectro_redux = cfg.get('namespace', 'desi_spectro_redux')

    exposure_zfill = str(exposure_id).zfill(8)
    expo_name = "desi-{}.fits.fz".format(exposure_zfill)

    file_path = os.path.join(desi_spectro_data, night, expo_name)

    try:
        hdr = astropy.io.fits.getheader(file_path)
    except Exception as err:
        logger.error("Error to load fits file: %s" % err)
        return {}

    # TODO: improve after understanding the QL pipeline cycle.
    program = hdr.get('program')
    program_file = program_mapping.get(program, 'darksurvey')

    config_file = cfg.get('main', 'qlconfig').format(program_file)
    current_config = change_config_file(config_file)

    return {
        "exposure_id": exposure_id,
        "dateobs": hdr.get('date-obs'),
        "night": night,
        "zfill": exposure_zfill,
        "desi_spectro_data": desi_spectro_data,
        "desi_spectro_redux": desi_spectro_redux,
        'telra': hdr.get('telra', None),
        'teldec': hdr.get('teldec', None),
        'tile': hdr.get('tileid', None),
        'flavor': hdr.get('flavor', None),
        'program': hdr.get('program', None),
        'airmass': hdr.get('airmass', None),
        'exptime': hdr.get('exptime', None),
        'qlconfig': current_config,
        'time': datetime.datetime.utcnow()
    }
