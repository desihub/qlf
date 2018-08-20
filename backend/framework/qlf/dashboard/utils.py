from astropy.time import Time
import os
from astropy.io import fits
import logging

from .models import Exposure

qlf_root = os.getenv('QLF_ROOT')

logger = logging.getLogger()

desi_spectro_redux = os.environ.get('DESI_SPECTRO_REDUX')
desi_spectro_data = os.environ.get('DESI_SPECTRO_DATA')


def get_date(exp):

    exposure = Exposure.objects.get(exposure_id=exp)

    if not exposure or not exposure.dateobs:
        return None

    time = str(exposure.dateobs)

    return Time(time, format='iso', scale='utc')
