import os
import sys
import configparser
from astropy.io import fits
import logging

logger = logging.getLogger(__name__)


class DOSmonitor(object):

    def __init__(self):

        qlf_root = os.getenv('QLF_ROOT')
        self.cfg = configparser.ConfigParser()
        try:
            self.cfg.read('%s/qlf/config/qlf.cfg' % qlf_root)
            self.desi_spectro_data = os.path.normpath(self.cfg.get('namespace', 'desi_spectro_data'))
        except Exception as error:
            logger.error(error)
            logger.error("Error reading  %s/qlf/config/qlf.cfg" % qlf_root)
            sys.exit(1)

        self.cameras = self.get_cameras()

    def get_nights(self):
        """ Gets nights """

        nights = self.cfg.get("data", "night")

        if not nights:
            return []

        return sorted(nights.split(','))

    def get_last_night(self):
        """ Gets last night """
        nights = self.cfg.get("data", "night")

        if not nights:
            return []

        return sorted(nights.split(','))[-1]

    def get_exposures_by_night(self, night):
        """ Gets exposures by night """

        exposures_list = list()

        exposures = self.cfg.get("data", "exposures").split(',')

        for expid in exposures:
            try:
                exposure = self.get_exposure(night, expid)
                if exposure:
                    exposures_list.append(exposure)
            except Exception as error:
                logger.error(error)

        return exposures_list

    def get_cameras(self):
        """ Gets all cameras from configuration file. """

        arms = self.cfg.get('data', 'arms').split(',')
        spectrographs = self.cfg.get('data', 'spectrographs').split(',')

        cameras = list()

        for arm in arms:
            for spec in spectrographs:
                try:
                    cameras.append(arm + spec)
                except Exception as error:
                    logger.error(error)

        return cameras

    def get_exposure(self, night, exposure):
        """ Gets all data of a determinate exposure. """

        exponame = "desi-%s.fits.fz" % str(exposure).zfill(8)
        filepath = os.path.join(self.desi_spectro_data, night, exponame)

        if not os.path.isfile(filepath):
            logger.error("exposure not found: %s" % filepath)
            return {}

        camera_list = list()

        for camera in self.cameras:

            camera_dict = {
                "name": camera,
            }
            camera_list.append(camera_dict)

        exposure_info = self.get_exposure_info(filepath, night)

        exposure_dict = {
            "night": night,
            "expid": exposure,
            "zfill": str(exposure).zfill(8),
            "desi_spectro_data": self.desi_spectro_data,
            "cameras": camera_list
        }

        exposure_dict.update(exposure_info)
        return exposure_dict

    def get_exposure_info(self, filepath, night):
        """ """

        try:
            fitsfile = fits.open(filepath)
            hdr = fitsfile[0].header
        except Exception as error:
            logger.error("error to load fits file: %s" % error)
            return {}

        dateobs = "%s-%s-%s 22:00" % (night[:-4], night[-4:][:2], night[-2:])

        return {
            'telra': hdr.get('telra', None),
            'teldec': hdr.get('teldec', None),
            'tile': hdr.get('tileid', None),
            #'dateobs': hdr.get('date-obs', None),
            'dateobs': dateobs,
            'flavor': hdr.get('flavor', None),
            'exptime': hdr.get('exptime', None)
        }


if __name__ == "__main__":
    dos_monitor = DOSmonitor()
    night = dos_monitor.get_last_night()
    exposures = dos_monitor.get_exposures_by_night(night)
    logger.info(exposures)
