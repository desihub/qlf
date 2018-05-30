import sys
import os
from astropy.io import fits
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html


class Fits2png:
    def __init__(self, cam):
        self.cam = cam

    def convert_fits2png(self):
        if isinstance(self.cam, str) and self.cam[0] in ['b', 'r', 'z'] and int(self.cam[1]) in range(10):
            pass
        else:
            return 'Invalid cam value or format'

        f = '/app/spectro/base_exposures/fiberflat/fiberflat-{}-{}.fits'.format(self.cam, str(1).zfill(8))

        img = fits.open(f)
        img0 = img[0]
        p = figure(
            x_range=(0, img0.data.shape[0]-1), y_range=(0, img0.data.shape[1]-1))
        p.image(image=[img0.data], x=0, y=0, dw=img0.data.shape[0] -
                1, dh=img0.data.shape[1]-1, palette="Spectral11")
        return file_html(p, CDN, "png")
