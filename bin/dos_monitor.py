import os
import sys
import configparser
import re


class DOSmonitor(object):

    def __init__(self):

        qlf_root = os.getenv('QLF_ROOT')
        self.cfg = configparser.ConfigParser()
        try:
            self.cfg.read('%s/qlf/config/qlf.cfg' % qlf_root)
            self.datadir = os.path.normpath(self.cfg.get('namespace', 'datadir'))
        except Exception as error:
            print(error)
            print("Error reading  %s/qlf/config/qlf.cfg" % qlf_root)
            sys.exit(1)
        
        self.cameras = self.get_cameras()

    def get_last_night(self):
        """ Gets last night """

        return self.cfg.get("data", "night")

    def get_exposures_by_night(self, night):
        """ Gets exposures by night """

        exposures_list = list()

        calib = self.cfg.get("data", "calib")
        exposures = self.cfg.get("data", "exposures").split(',')

        for expid in exposures:
            try:
                exposure = self.get_exposure(night, expid, calib)
                exposures_list.append(exposure)
            except Exception as error:
                print(error)
                sys.exit(1)

        return exposures_list

    def get_cameras(self):
        """ Gets all cameras from configuration file. """

        arms = self.cfg.get('data', 'arm').split(',')
        spectrographs = self.cfg.get('data', 'spectrograph').split(',')

        cameras = list()

        for arm in arms:
            for spec in spectrographs:
                try:
                    cameras.append(arm + spec)
                except Exception as error:
                    print(error)

        return cameras

    def get_exposure(self, night, exposure, calib):
        """ Gets all data of a determinate exposure. """

        camera_list = list()

        for camera in self.cameras:
            try:
                fiberflat = self.get_fiberflat_file(night, calib, camera)
                psfboot = self.get_psfboot_file(night, camera)
            except Exception as error:
                print(error)
                continue

            camera_dict = {
                "name": camera,
                "psfboot": psfboot,
                "fiberflat": fiberflat
            }
            camera_list.append(camera_dict)

        return {
            "night": night,
            "expid": exposure,
            "zfill": str(exposure).zfill(8),
            "data_dir": self.datadir,
            "cameras": camera_list
        }

    def get_fiberflat_file(self, night, calib, camera):
        """ Gets the fiberflat file by camera """

        path = os.path.join(self.datadir, night)
        calib = str(calib).zfill(8)

        pattern = "(fiberflat-%s-%s.fits)" % (camera, calib)
        regex = re.compile(pattern)

        for f in os.listdir(path):
            if regex.search(f):
                return os.path.join(path, f)

        raise OSError(2, 'fiberflat not found', pattern)

    def get_psfboot_file(self, night, camera):
        """ Gets the psfboot file by camera """

        path = os.path.join(self.datadir, night)

        pattern = "(psfboot-%s.fits)" % camera
        regex = re.compile(pattern)

        for f in os.listdir(path):
            if regex.search(f):
                return os.path.join(path, f)

        raise OSError(2, 'psfboot not found', pattern)

if __name__ == "__main__":

    dos_monitor = DOSmonitor()
    night = dos_monitor.get_last_night()
    exposures = dos_monitor.get_exposures_by_night(night)
    print(exposures)
