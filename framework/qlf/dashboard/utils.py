from astropy.time import Time
import os
import configparser
from astropy.io import fits

qlf_root = os.getenv('QLF_ROOT')
cfg = configparser.ConfigParser()

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
    exp_zfill = str(exp).zfill(8)
    fits_file = '{}/{}/desi-{}.fits.fz'.format(desi_spectro_data, night, exp_zfill)

    f = fits.open(fits_file)

    # read the time in isot
    time = f[0].header['DATE-OBS']

    # declare the format
    t = Time(time, format='isot', scale='utc')

    # Convert to MJD
    return t