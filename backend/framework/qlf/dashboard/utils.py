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

    exposure = Exposure.objects.get(exposure_id=exp)

    if not exposure or not exposure.dateobs:
        return None

    time = str(exposure.dateobs)

    return Time(time, format='iso', scale='utc')
