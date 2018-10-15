import os
from astropy.io import fits
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html
from bokeh.models import LogColorMapper, ColorMapper
import numpy as np

desi_spectro_data = os.environ.get('DESI_SPECTRO_DATA')
desi_spectro_redux = os.environ.get('DESI_SPECTRO_REDUX')


class Fits2png:
    def __init__(self, cam, processing, night, exposure):
        self.cam = cam
        self.processing = processing
        self.night = night
        self.exposure = exposure

    def convert_fits2png(self):
        exp_zfill = str(self.exposure).zfill(8)

        if self.processing == 'raw':
            f = '{}/{}/{}/desi-{}.fits.fz'.format(desi_spectro_data,
                                                  self.night, exp_zfill,
                                                  exp_zfill)
        elif self.processing == 'reduced':
            f = '{}/exposures/{}/{}/sframe-{}-{}.fits'.format(
                desi_spectro_redux, self.night, exp_zfill, self.cam, exp_zfill)
        else:
            return 'Invalid processing option'

        try:
            img = fits.open(f)
        except FileNotFoundError:
            return 'File not found'

        if self.processing == 'raw':
            offset = 0
            if self.cam[0] == 'r':
                offset = 10
            if self.cam[0] == 'z':
                offset = 20
            img_data = img[offset+int(self.cam[1])+1]
            low = np.amin(img_data.data)
            high = np.amax(img_data.data)
            color_mapper = LogColorMapper(
                palette="Greys256", low=low, high=high)
            p = figure(
                x_range=(0, img_data.data.shape[0]-1), y_range=(0, img_data.data.shape[1]-1))
            p.image(image=[img_data.data], x=0, y=0, dw=img_data.data.shape[0] -
                    1, dh=img_data.data.shape[1]-1, color_mapper=color_mapper)
        else:
            img_data = img[1]
            p = figure(
                x_range=(0, img_data.data.shape[0]-1), y_range=(0, img_data.data.shape[1]-1))
            p.image(image=[img_data.data], x=0, y=0, dw=img_data.data.shape[0] -
                    1, dh=img_data.data.shape[1]-1, palette="Greys256")

        return file_html(p, CDN, "png")
