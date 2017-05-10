import configparser
import re
import os


class DOSlib():

    def __init__(self):
        self.cfg = configparser.ConfigParser()
        project_path = os.getenv('QLF_PROJECT')

        print(project_path)

        self.cfg.read('%s/config/qlf.cfg' % project_path)
        self.datadir = os.path.normpath(self.cfg.get(
            'namespace',
            'datadir'
        ))

        self.cameras = self.get_cameras()

    def get_cameras(self):
        """ """
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
        """ """

        camera_list = list()

        for camera in self.cameras:
            fiberflat = self.get_fiberflat_file(night, exposure, camera)
            psfboot = self.get_psfboot_file(night, camera)
            camera_dict = {
                "name": camera,
                "psfboot": psfboot,
                "fiberflat": fiberflat
            }
            camera_list.append(camera_dict)

        return {
            "night": night,
            "expid": exposure,
            "raw_dir": self.datadir,
            "cameras": camera_list
        }

    def get_fiberflat_file(self, night, exposure, camera):
        """ """

        path = os.path.join(self.datadir, night)
        exposure = str(exposure).zfill(8)

        pattern = "(fiberflat-%s-%s.fits)" % (camera, exposure)
        regex = re.compile(pattern)

        for f in os.listdir(path):
            if regex.search(f):
                return os.path.join(path, f)

        raise OSError(2, 'fiberflat not found', pattern)

    def get_psfboot_file(self, night, camera):
        """ """

        path = os.path.join(self.datadir, night)

        pattern = "(psfboot-%s.fits)" % camera
        regex = re.compile(pattern)

        for f in os.listdir(path):
            if regex.search(f):
                return os.path.join(path, f)

        raise OSError(2, 'psfboot not found', pattern)

    # def get_raw_files(self, night, exposure):
    #     """ """
    #
    #     path = os.path.join(self.datadir, night)
    #
    #     pattern = "(desi-[0]+%i)" % int(exposure)
    #     regex = re.compile(pattern)
    #     return [f for f in os.listdir(path) if regex.search(f)]


