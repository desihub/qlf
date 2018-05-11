from astropy.time import Time
import os
import configparser
from astropy.io import fits
import logging

from .models import Exposure

qlf_root = os.getenv('QLF_ROOT')
cfg = configparser.ConfigParser()

logger = logging.getLogger()

try:
    cfg.read('%s/framework/config/qlf.cfg' % qlf_root)
    desi_spectro_redux = cfg.get('namespace', 'desi_spectro_redux')
    desi_spectro_data = cfg.get('namespace', 'desi_spectro_data')
    night = cfg.get('data', 'night')
except Exception as error:
    logger.error(error)
    logger.error("Error reading  %s/framework/config/qlf.cfg" % qlf_root)


def get_date(exp):

    # open file
    # exp_zfill = str(exp).zfill(8)

    exposure = Exposure.objects.get(exposure_id=exp)

    # fits_file = '{}/{}/desi-{}.fits.fz'.format(
    #     desi_spectro_data,
    #     exposure.night,
    #     exp_zfill
    # )
    #
    # try:
    #     f = fits.open(fits_file)
    # except FileNotFoundError:
    #     logger.exception('Fits file not found: {}'.format(fits_file))
    #     return None
    #
    # # read the time in isot
    # time = f[0].header['DATE-OBS']

    t = None

    if exposure and exposure.dateobs:
        time = exposure.dateobs
        # declare the format
        try:
            t = Time(time, format='isot', scale='utc')
        except Exception:
            print(time)
            logger.info(time)
            logger.exception('Error to get time.')
            t = None

    # Convert to MJD
    return t



