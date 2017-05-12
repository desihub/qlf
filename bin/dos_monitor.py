import configparser
import re
import os


class DOSmonitor(object):

    def __init__(self):
        project_path = os.getenv('QLF_ROOT')

        self.cfg = configparser.ConfigParser()
        self.cfg.read('%s/config/qlf.cfg' % project_path)

        self.datadir = os.path.normpath(self.cfg.get(
            'namespace',
            'rawdir'
        ))

        self.cameras = self.get_cameras()

    def get_last_night(self):
        """ Gets last night """

        return self.cfg.get("data", "night")

    def get_exposures_by_night(self, night):
        """ Gets exposures by night """

        exposures_list = list()

        exposures = self.cfg.get("data", "exposures").split(',')

        for expid in exposures:
            try:
                exposure = self.get_exposure(night, expid)
                exposures_list.append(exposure)
            except Exception as error:
                print(error)

        return exposures_list

    def get_cameras(self):
        """ Gets all cameras from configuration file. """

        arms = self.cfg.get('cameras', 'arm').split(',')
        spectrographs = self.cfg.get('cameras', 'spectrograph').split(',')

        cameras = list()

        for arm in arms:
            for spec in spectrographs:
                try:
                    cameras.append(arm + spec)
                except Exception as error:
                    print(error)

        return cameras

    def get_exposure(self, night, exposure):
        """ Gets all data of a determinate exposure. """

        camera_list = list()

        for camera in self.cameras:
            try:
                fiberflat = self.get_fiberflat_file(night, exposure, camera)
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
            "raw_dir": self.datadir,
            "cameras": camera_list
        }

    def get_fiberflat_file(self, night, exposure, camera):
        """ Gets the fiberflat file by camera """

        path = os.path.join(self.datadir, night)
        exposure = str(exposure).zfill(8)

        pattern = "(fiberflat-%s-%s.fits)" % (camera, exposure)
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

    dosmonitor = DOSmonitor()
    night = dosmonitor.get_last_night()
    exposures = dosmonitor.get_exposures_by_night(night)
    print(exposures)
