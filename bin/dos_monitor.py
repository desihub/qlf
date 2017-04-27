import configparser
import re
import os


class DOSlib():

    def __init__(self):
        cfg = configparser.ConfigParser()
        project_path = os.getenv('QLF_PROJECT')
        cfg.read('%s/config/qlf.cfg' % project_path)
        self.datadir = os.path.normpath(cfg.get(
            'namespace',
            'datadir'
        ))

    def get_last_expid(self):
        """ """
        pass

    def get_exposure(self, night, exposure):
        """ """

        # TODO: in development

        path = os.path.join(self.datadir, night)
        raw_files = self.get_raw_files(night, exposure)
        fiberflat = self.get_fiberflat_file(night)
        fiberflat = fiberflat.pop()
        psfboot = self.get_psfboot_file(night)
        psfboot = psfboot.pop()
        camera = psfboot.split('-')[-1].split('.')[0]

        return {
            "night": night,
            "expid": exposure,
            "camera": camera,
            "path": path,
            "raw_files": raw_files,
            "psfboot": psfboot,
            "fiberflat": fiberflat
        }

    def get_raw_files(self, night, exposure):
        """ """

        path = os.path.join(self.datadir, night)

        pattern = "(([a-z]+)-[0]+%i)" % int(exposure)
        regex = re.compile(pattern)
        return [f for f in os.listdir(path) if regex.search(f)]

    def get_fiberflat_file(self, night):
        """ """

        path = os.path.join(self.datadir, night)

        pattern = "(fiberflat).*"
        regex = re.compile(pattern)
        return [f for f in os.listdir(path) if regex.search(f)]

    def get_psfboot_file(self, night):
        """ """

        path = os.path.join(self.datadir, night)

        pattern = "(psfboot).*"
        regex = re.compile(pattern)
        return [f for f in os.listdir(path) if regex.search(f)]
