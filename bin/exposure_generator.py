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
        self.min_interval = 10
        self.max_interval = 15

        self.spectro_path = None
        self.fiberflat_path = None
        self.psfboot_path = None

        self.base_night = None
        self.base_exposure = None
        self.all_cameras = None

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
        gen_time = datetime.datetime.now()
        exp_id = self.__genNewExpId()
        self.__genDesiFile(exp_id, gen_time)
        self.__genFibermapFile(exp_id, gen_time)
        self.__genFiberflatFolder(exp_id, gen_time)
        self.__genPsfbootFolder(exp_id, gen_time)

        return {
            "exp_id": exp_id,
            "date-obs": self.__dateObs(gen_time),
            "night": self.__nightToGenerate(gen_time)
        }

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

    def __genDesiFile(self, exp_id, gen_time):
        src = os.path.join(self.spectro_path, self.base_night)
        dest = os.path.join(
            self.spectro_path, self.__nightToGenerate(gen_time))
        self.__ensureDir(dest)
        src_file = os.path.join(
            src, ("desi-%s.fits.fz" % (self.base_exposure)))
        dest_file = os.path.join(dest, ("desi-%s.fits.fz" % (exp_id)))
        shutil.copy(src_file, dest_file)
        self.__updateFITSFileMetadata(dest_file, exp_id, gen_time)

    def __nightToGenerate(self, gen_time):
        return (gen_time - datetime.timedelta(hours=12)).strftime("%Y%m%d")

    def __dateObs(self, gen_time):
        return gen_time.strftime("%Y-%m-%dT%H:%M:%S")

    def __ensureDir(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def __updateFITSFileMetadata(self, exp_file, exp_id, gen_time):
        hdulist = astropy.io.fits.open(exp_file, mode="update")
        for hduid in range(0, len(hdulist)):
            if "EXPID" in hdulist[hduid].header:
                hdulist[hduid].header["EXPID"] = (
                    int(exp_id))
            if "DATE-OBS" in hdulist[hduid].header:
                hdulist[hduid].header["DATE-OBS"] = (
                    self.__dateObs(gen_time))
            if "NIGHT" in hdulist[hduid].header:
                hdulist[hduid].header["NIGHT"] = (
                    self.__nightToGenerate(gen_time))
            if "ARCNIGHT" in hdulist[hduid].header:
                hdulist[hduid].header["ARCNIGHT"] = (
                    self.__nightToGenerate(gen_time))
            if "FLANIGHT" in hdulist[hduid].header:
                hdulist[hduid].header["FLANIGHT"] = (
                    self.__nightToGenerate(gen_time))
        hdulist.flush()
        hdulist.close()

    def __genFibermapFile(self, exp_id, gen_time):
        src = os.path.join(self.spectro_path, self.base_night)
        dest = os.path.join(
            self.spectro_path, self.__nightToGenerate(gen_time))
        self.__ensureDir(dest)
        src_file = os.path.join(
            src, ("fibermap-%s.fits" % (self.base_exposure)))
        dest_file = os.path.join(dest, ("fibermap-%s.fits" % (exp_id)))
        shutil.copy(src_file, dest_file)
        self.__updateFITSFileMetadata(dest_file, exp_id, gen_time)

    def __genFiberflatFolder(self, exp_id, gen_time):
        src = os.path.join(self.fiberflat_path, self.base_night)
        dest = os.path.join(
            self.fiberflat_path, self.__nightToGenerate(gen_time))

        self.__ensureDir(dest)
        regex = re.compile("^(fiberflat-\w+-)(\d{8})(.fits)$")

        for filename in os.listdir(src):
            src_file = os.path.join(src, filename)
            new_filename = regex.sub("\g<1>" + exp_id + "\g<3>", filename)
            dest_file = os.path.join(dest, new_filename)
            shutil.copy(src_file, dest_file)

            self.__updateFITSFileMetadata(dest_file, exp_id, gen_time)

    def __genPsfbootFolder(self, exp_id, gen_time):
        # it is fine to just copy the path
        src = os.path.join(self.psfboot_path, self.base_night)
        dest = os.path.join(
            self.psfboot_path, self.__nightToGenerate(gen_time))

        if not os.path.exists(dest):
            shutil.copytree(src, dest)

            for filename in os.listdir(dest):
                dest_file = os.path.join(dest, filename)
                self.__updateFITSFileMetadata(dest_file, exp_id, gen_time)

    def printVars(self):
        log.info("min_interval:      %s" % self.min_interval)
        log.info("max_interval:      %s" % self.max_interval)

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
        print("Starting generation of new exposure...")
        result = eg.generateExposure()
        print(
            "Exposure id '%s' generated at '%s' as night '%s'."
            % (result['exp_id'], result['date-obs'], result['night'])
        )
        rand = random.randint(eg.min_interval, eg.max_interval)
        print("Next generation in %s minutes..." % rand)
        time.sleep(rand * 60)

    # TODO add a function to cleanup generated files
