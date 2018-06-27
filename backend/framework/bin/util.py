import logging
import configparser
import os
import astropy.io.fits
import datetime
import yaml
from qlf_models import QLFModels

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


def change_config_file(night, exposure_id, program):
    """ Makes a copy of the original configuration file by modifying
    some values defined in qlf.cfg.

    Arguments:
        night {str} -- night
        exposure_id {int} -- exposure ID
        program {str} -- program

    Returns:
        str -- config file path that will be used
    """

    cfg = get_config()

    program_file = program_mapping.get(program, 'darksurvey')
    config_file = cfg.get('main', 'qlconfig').format(program_file)

    models = QLFModels()
    template = models.get_last_exposure_by_program(program)

    with open(config_file, 'r') as file:
        config = yaml.load(file)

    psf_exp_id = cfg.getint("pipeline", "psf_exp_id")
    fiberflat_exp_id = cfg.getint("pipeline", "fiberflat_exp_id")
    use_resolution = cfg.getboolean("pipeline", "use_resolution")
    write_intermediate_files = cfg.getboolean(
        "pipeline",
        "write_intermediate_files"
    )

    if config.get('PSFExpid', None):
        config['PSFExpid'] = psf_exp_id

    if config.get('FiberflatExpid', None):
        config['FiberflatExpid'] = fiberflat_exp_id

    if config.get('UseResolution', None):
        config['UseResolution'] = use_resolution

    if config.get('WriteIntermediatefiles', None):
        config['WriteIntermediatefiles'] = write_intermediate_files

    if template:
        if config.get('TemplateNight', None):
            config['TemplateNight'] = int(template.night)

        if config.get('TemplateExpid', None):
            config['TemplateExpid'] = template.exposure_id

    desi_spectro_redux = cfg.get('namespace', 'desi_spectro_redux')
    config_path = os.path.join(desi_spectro_redux, 'exposures', night)

    ensure_dir(config_path)

    current_config = os.path.join(config_path, os.path.basename(config_file))

    with open(current_config, 'w') as file:
        yaml.dump(config, file)

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

    file_path = os.path.join(desi_spectro_data, night, exposure_zfill, expo_name)

    try:
        hdr = astropy.io.fits.getheader(file_path)
    except Exception as err:
        logger.error("Error to load fits file: %s" % err)
        return {}

    # TODO: improve after understanding the QL pipeline cycle.
    program = hdr.get('program')

    current_config = change_config_file(night, exposure_id, program)
    define_calibration_files(night)

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


def define_calibration_files(night):
    """ Sets the night calibration files

    Arguments:
        night {str} -- night
    """

    cfg = get_config()
    spectro_redux = cfg.get("namespace", "desi_spectro_redux")
    calib_path = cfg.get("namespace", "calibration_path")
    dest = os.path.join(spectro_redux, "exposures", night)

    psf_exp_id = cfg.get("pipeline", "psf_exp_id")
    fiberflat_exp_id = cfg.get("pipeline", "fiberflat_exp_id")

    ensure_dir(dest)

    links = [
        ('psf', psf_exp_id.zfill(8)),
        ('fiberflat', fiberflat_exp_id.zfill(8))
    ]

    for item in links:
        item_path = os.path.join(calib_path, item[0])
        dest_item = os.path.join(dest, item[1])

        if not os.path.islink(dest_item):
            os.symlink(item_path, dest_item)


def ensure_dir(path):
    """ Ensures that the directory exists.

    Arguments:
        path {str} -- directory path
    """

    os.makedirs(path, exist_ok=True)


def format_night(new_date):
    return new_date.strftime("%Y%m%d")
