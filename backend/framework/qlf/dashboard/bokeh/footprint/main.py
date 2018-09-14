import astropy
from astropy.table import Table
from astropy import units as u
from astropy.coordinates import SkyCoord, EarthLocation, AltAz
from astropy.time import Time

from bokeh.plotting import figure
from bokeh.layouts import widgetbox, row, column
from bokeh.models import Div, Panel, Tabs
from bokeh.resources import CDN
from bokeh.embed import file_html
import os

from dashboard.models import Exposure

# from log import get_logger

# qlf_root = os.environ.get('QLF_ROOT')

# logger = get_logger(
#     "qlf.bokeh",
#     os.path.join(qlf_root, "logs", "bokeh.log")
# )

class Footprint():
    def footprint(self, coords, visibles):

        x = coords.ra*u.hour
        y = coords.dec*u.deg

        vx = visibles.ra*u.hour
        vy = visibles.dec*u.deg

        plot = figure(tools='pan,wheel_zoom,reset,lasso_select,crosshair')

        plot.circle(x, y, fill_color='blue', alpha=0.5)

        plot.circle(vx, vy, fill_color='red', size=5, alpha=0.7)

        plot.xaxis.axis_label = "RA (deg)"
        plot.yaxis.axis_label = "DEC (deg)"

        return plot

    def render(self, exposures):
        pointings_file = os.environ.get(
            'POINTINGS_FILE', '/app/spectro/noconstraints.dat')

        # you need to edit the original file to comment the header and join hourangle
        pointings = Table.read(pointings_file, format='ascii.commented_header')
        exp = Exposure.objects.last()
        coords = SkyCoord(ra=pointings['RA']*u.hour,
                          dec=pointings['DEC']*u.deg, frame='icrs')
        if not exposures:
            empty = SkyCoord(ra=[]*u.hour, dec=[]*u.deg, frame='icrs')
            return file_html(self.footprint(coords, empty), CDN, "DESI Footprint")
        visibles = SkyCoord(ra=exposures.values_list('telra')*u.hour,
                            dec=exposures.values_list('teldec')*u.deg, frame='icrs')

        return file_html(self.footprint(coords, visibles), CDN, "DESI Footprint")
