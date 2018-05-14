import astropy.io.fits
import datetime
from log import get_logger
import os
import random
import re
import shutil
import time
from util import get_config
from multiprocessing import Process, Manager

cfg = get_config()
qlf_root = cfg.get("environment", "qlf_root")

log = get_logger(
    "exposure.generator",
    os.path.join(qlf_root, "logs", "exposure_generator.log")
)

spectro_path = os.path.normpath(cfg.get("namespace", "desi_spectro_data"))
spectro_redux = os.path.normpath(cfg.get("namespace", "desi_spectro_redux"))
fiberflat_path = os.path.join(spectro_redux, "calib2d")
psfboot_path = os.path.join(fiberflat_path, "psf")
list_base_nights = cfg.get("data", "night").split(",")
min_interval = cfg.getint("main", "min_interval")
max_interval = cfg.getint("main", "max_interval")
max_exposures = cfg.getint("main", "max_exposures")


class ExposureGenerator(Process):

    def __init__(self):
        super().__init__()

        self.__last_exposure = Manager().dict()
        self.__cameras = list()
        self.__base_night = None
        self.__base_exposure = None
        self.__generation_count = 0

        arms = cfg.get('data', 'arms').split(',')
        spectrographs = cfg.get('data', 'spectrographs').split(',')

        for arm in arms:
            for spec in spectrographs:
                self.__cameras.append({'name': arm + spec})

    @staticmethod
    def __get_random_night():
        """ """

        return random.choice(list_base_nights)

    def __get_random_exposure(self):

        nights_path = os.path.join(spectro_path, self.__base_night)

        if not os.path.exists(nights_path):
            log.error("Directory does not exist: {}".format(nights_path))
            raise OSError

        exposures_list = re.findall(
            "desi-(\d+).fits.fz",
            ''.join(os.listdir(nights_path))
        )

        return random.choice(exposures_list)

    def run(self):
        while self.__generation_count < max_exposures:
            log.info("Starting generation of new exposure...")

            last_exposure = self.generate_exposure()
            log.info(
                "Exposure id '%s' generated at '%s' as night '%s'."
                % (last_exposure['expid'], last_exposure['dateobs'], last_exposure['night'])
            )

            self.__last_exposure.update(last_exposure)
            self.__generation_count += 1

            if self.__generation_count == max_exposures:
                continue

            rand = random.randint(min_interval, max_interval)
            log.info("Next generation in %s minutes..." % rand)

            time.sleep(rand * 60)

    def get_last_exposure(self):
        return Manager().dict(self.__last_exposure)

    def generate_exposure(self):
        self.__base_night = self.__get_random_night()
        self.__base_exposure = self.__get_random_exposure()

        log.info("Base night: {}".format(self.__base_night))
        log.info("Base exposure: {}".format(self.__base_exposure))

        gen_time = datetime.datetime.now()
        exp_id = self.__gen_new_expid()
        exp_id_zfill = str(exp_id).zfill(8)

        self.__gen_desi_file(exp_id_zfill, gen_time)
        self.__gen_fibermap_file(exp_id_zfill, gen_time)
        self.__gen_fiberflat_folder(gen_time)
        self.__gen_psfboot_folder(gen_time)

        expo_name = "desi-{}.fits.fz".format(exp_id_zfill)
        night = self.__night_to_generate(gen_time)
        file_path = os.path.join(spectro_path, night, expo_name)

        try:
            hdr = astropy.io.fits.getheader(file_path)
        except Exception as err:
            log.error("error to load fits file: %s" % err)
            return {}

        return {
            "expid": exp_id,
            "dateobs": self.__date_obs(gen_time),
            "night": night,
            "zfill": exp_id_zfill,
            "desi_spectro_data": spectro_path,
            "desi_spectro_redux": spectro_redux,
            "cameras": self.__cameras,
            'telra': hdr.get('telra', None),
            'teldec': hdr.get('teldec', None),
            'tile': hdr.get('tileid', None),
            'flavor': hdr.get('flavor', None),
            'exptime': hdr.get('exptime', None),
            'time': datetime.datetime.utcnow()
        }

    def __gen_new_expid(self):
        last_id = self.__get_last_expid()

        return int(last_id) + 1

    def __get_last_expid(self):
        # spectro 'desi-X.fits.fz' is mandatory,
        # so should be fine to use it to detect the last exp_id

        last_night = self.__get_last_night()

        listdir = os.listdir(os.path.join(spectro_path, last_night))
        regex = re.compile("^desi-\d+.fits.fz$")
        last_exp_file = sorted(list(filter(regex.match, listdir)))[-1]

        return re.findall("^desi-(\d+).fits.fz$", last_exp_file)[0]

    def __get_last_night(self):
        listdir = os.listdir(spectro_path)
        regex = re.compile("^\d+$")
        regex_match = list(filter(regex.match, listdir))

        # last night can not be detected, because the 'demo' night
        # is dated on 2019, so it will be the last night until 2019 comes
        if len(regex_match) > 1 and regex_match.count("20190101"):
            regex_match.remove("20190101")

        return sorted(regex_match)[-1]

    def __gen_desi_file(self, exp_id, gen_time):
        src = os.path.join(spectro_path, self.__base_night)
        dest = os.path.join(
            spectro_path, self.__night_to_generate(gen_time))
        self.__ensure_dir(dest)
        src_file = os.path.join(
            src, ("desi-{}.fits.fz".format(self.__base_exposure)))
        dest_file = os.path.join(dest, ("desi-{}.fits.fz".format(exp_id)))
        shutil.copy(src_file, dest_file)
        self.__update_fitsfile_metadata(dest_file, exp_id, gen_time)

    def __update_fitsfile_metadata(self, exp_file, exp_id, gen_time):
        hdulist = astropy.io.fits.open(exp_file, mode="update")
        for hduid in range(0, len(hdulist)):
            if "EXPID" in hdulist[hduid].header:
                hdulist[hduid].header["EXPID"] = (
                    int(exp_id))
            if "DATE-OBS" in hdulist[hduid].header:
                hdulist[hduid].header["DATE-OBS"] = (
                    self.__date_obs(gen_time))
            if "NIGHT" in hdulist[hduid].header:
                hdulist[hduid].header["NIGHT"] = (
                    self.__night_to_generate(gen_time))
            if "ARCNIGHT" in hdulist[hduid].header:
                hdulist[hduid].header["ARCNIGHT"] = (
                    self.__night_to_generate(gen_time))
            if "FLANIGHT" in hdulist[hduid].header:
                hdulist[hduid].header["FLANIGHT"] = (
                    self.__night_to_generate(gen_time))
        hdulist.flush()
        hdulist.close()

    def __gen_fibermap_file(self, exp_id, gen_time):
        src = os.path.join(spectro_path, self.__base_night)
        dest = os.path.join(
            spectro_path, self.__night_to_generate(gen_time))
        self.__ensure_dir(dest)
        src_file = os.path.join(
            src, ("fibermap-{}.fits".format(self.__base_exposure)))
        dest_file = os.path.join(dest, ("fibermap-{}.fits".format(exp_id)))
        shutil.copy(src_file, dest_file)
        self.__update_fitsfile_metadata(dest_file, exp_id, gen_time)

    def __gen_fiberflat_folder(self, gen_time):
        src = os.path.join(fiberflat_path, self.__base_night)
        dest = os.path.join(
            fiberflat_path, self.__night_to_generate(gen_time))

        self.__ensure_dir(dest)

        if not os.listdir(dest):
            for filename in os.listdir(src):
                if not filename.endswith(".fits"):
                    continue

                src_file = os.path.join(src, filename)
                dest_file = os.path.join(dest, filename)
                shutil.copy(src_file, dest_file)

    def __gen_psfboot_folder(self, gen_time):
        # it is fine to just copy the path
        src = os.path.join(psfboot_path, self.__base_night)
        dest = os.path.join(
            psfboot_path, self.__night_to_generate(gen_time))

        if not os.path.exists(dest):
            shutil.copytree(src, dest)

    @staticmethod
    def __night_to_generate(gen_time):
        return (gen_time - datetime.timedelta(hours=12)).strftime("%Y%m%d")

    @staticmethod
    def __date_obs(gen_time):
        return gen_time.strftime("%Y-%m-%dT%H:%M:%S")

    @staticmethod
    def __ensure_dir(path):
        if not os.path.exists(path):
            os.makedirs(path)

    def __print_vars(self):
        log.info("min_interval:      {}".format(min_interval))
        log.info("max_interval:      {}".format(max_interval))
        log.info("spectro_path:      {}".format(spectro_path))
        log.info("fiberflat_path:    {}".format(fiberflat_path))
        log.info("psfboot_path:      {}".format(psfboot_path))


if __name__ == "__main__":
    print('Start Exposure Generator...')
    generator = ExposureGenerator()
    generator.start()
