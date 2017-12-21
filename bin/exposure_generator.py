import astropy.io.fits
import configparser
import datetime
import logging
import os
import random
import re
import shutil
import sys
import time


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
sh = logging.StreamHandler(sys.stdout)
sh.setLevel(logging.DEBUG)
log.addHandler(sh)


class ExposureGenerator(object):

    def __init__(self):
        self.min_interval = 5 * 60
        self.max_interval = 10 * 60
        self.night_to_generate = datetime.date.today().strftime("%Y%m%d")

        self.__getConfigs()

    def __getConfigs(self):
        qlf_root = os.getenv("QLF_ROOT")
        qlf_conf = os.path.join(qlf_root, "qlf/config/qlf.cfg")

        cfg = configparser.ConfigParser()

        try:
            cfg.read(qlf_conf)

            self.spectro_path = os.path.normpath(
                cfg.get("namespace", "desi_spectro_data"))
            desi_spectro_redux = os.path.normpath(
                cfg.get("namespace", "desi_spectro_redux"))

            self.fiberflat_path = os.path.join(desi_spectro_redux, "calib2d")
            self.psfboot_path = os.path.join(self.fiberflat_path, "psf")

            self.base_night = cfg.get("data", "night").split(",")[0]
            self.base_exposure = self.__exposureFormat(
                int(cfg.get("data", "exposures").split(",")[0]))
            self.all_cameras = self.__getAllCameras()

        except Exception as error:
            log.error(error)
            log.error("Error reading config file %s" % qlf_conf)
            sys.exit(1)

    def __exposureFormat(self, id):
        return str("%08d") % (id,)

    def __getAllCameras(self):
        arms = ["b", "r", "z"]
        spectrographs = list(range(0, 10))
        cameras = list()

        for arm in arms:
            for spec in spectrographs:
                cameras.append(arm + str(spec))

        return cameras

    def generateExposure(self):
        exp_id = self.__genNewExpId()
        self.__genDesiFile(exp_id)
        self.__genFibermapFile(exp_id)
        self.__genFiberflatFolder(exp_id)
        self.__genPsfbootFolder(exp_id)

        return exp_id

    def __genNewExpId(self):
        last_id = self.__getLastExpId()

        return self.__exposureFormat(int(last_id) + 1)

    def __getLastExpId(self):
        # spectro 'desi-X.fits.fz' is mandatory,
        # so should be fine to use it to detect the last exp_id

        last_night = self.__getLastNight()

        l = os.listdir(os.path.join(self.spectro_path, last_night))
        r = re.compile("^desi-\d+.fits.fz$")
        last_exp_file = sorted(list(filter(r.match, l)))[-1]

        return re.findall("^desi-(\d+).fits.fz$", last_exp_file)[0]

    def __getLastNight(self):
        l = os.listdir(self.spectro_path)
        r = re.compile("^\d+$")
        m = list(filter(r.match, l))

        # last night can not be detected, because the 'demo' night
        # is dated on 2019, so it will be the last night until 2019 comes
        if len(m) > 1 and m.count("20190101"):
            m.remove("20190101")

        return sorted(m)[-1]

    def __genDesiFile(self, exp_id):
        src = os.path.join(self.spectro_path, self.base_night)
        dest = os.path.join(self.spectro_path, self.night_to_generate)
        self.__ensureDir(dest)
        src_file = os.path.join(
            src, ("desi-%s.fits.fz" % (self.base_exposure)))
        dest_file = os.path.join(dest, ("desi-%s.fits.fz" % (exp_id)))
        shutil.copy(src_file, dest_file)
        self.__updateExposureFileMetadata(dest_file, exp_id)

    def __ensureDir(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def __updateExposureFileMetadata(self, exp_file, exp_id):
        hdulist = astropy.io.fits.open(exp_file, mode="update")
        for hduid in range(0, len(hdulist)):
            if 'EXPID' in hdulist[hduid].header:
                hdulist[hduid].header['EXPID'] = exp_id
        hdulist.flush()
        hdulist.close()

    def __genFibermapFile(self, exp_id):
        src = os.path.join(self.spectro_path, self.base_night)
        dest = os.path.join(self.spectro_path, self.night_to_generate)
        self.__ensureDir(dest)
        shutil.copy(
            os.path.join(src, ("fibermap-%s.fits" % (self.base_exposure))),
            os.path.join(dest, ("fibermap-%s.fits" % (exp_id))))

    def __genFiberflatFolder(self, exp_id):
        # actually just copy the path
        # TODO check if the 00000001 part of the filename should be updated
        src = os.path.join(self.fiberflat_path, self.base_night)
        dest = os.path.join(self.fiberflat_path, self.night_to_generate)

        if not os.path.exists(dest):
            shutil.copytree(src, dest)

    def __genPsfbootFolder(self, exp_id):
        # it is fine to just copy the path
        src = os.path.join(self.psfboot_path, self.base_night)
        dest = os.path.join(self.psfboot_path, self.night_to_generate)

        if not os.path.exists(dest):
            shutil.copytree(src, dest)

    def printVars(self):
        log.info("min_interval:      %s" % self.min_interval)
        log.info("max_interval:      %s" % self.max_interval)
        log.info("night_to_generate: %s" % self.night_to_generate)

        log.info("spectro_path:      %s" % self.spectro_path)
        log.info("fiberflat_path:    %s" % self.fiberflat_path)
        log.info("psfboot_path:      %s" % self.psfboot_path)

        log.info("base_night:        %s" % self.base_night)
        log.info("base_exposure:     %s" % self.base_exposure)
        log.info("all_cameras:       %s" % self.all_cameras)


if __name__ == "__main__":
    eg = ExposureGenerator()
    eg.printVars()

    while True:
        rand = random.randint(10, 15)
        print("Next generation in %s minutes..." % rand)
        time.sleep(rand * 60)
        print(
            "Generated exposure id '%s'."
            % eg.generateExposure()
        )

    # TODO change the MJD header to the time of generation

    # TODO change the generated folder to the date of generation

    # TODO add a function to cleanup generated files
