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

class Footprint():
    def select_exposures(self, coords, observing_time, observing_location, altcut=85*u.deg):
        '''For a given night and altitude cut select handful of visible exposures
        return coordinates of visible objects'''

        aa = AltAz(location=observing_location, obstime=observing_time)
        coords_aa = coords.transform_to(aa)
        visibles = coords[coords_aa.alt > altcut]

        return visibles


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

    def render(self):
        pointings_file = os.environ.get(
            'POINTINGS_FILE', '/app/spectro/noconstraints.dat')

        # you need to edit the original file to comment the header and join hourangle
        pointings = Table.read(pointings_file, format='ascii.commented_header')
        coords = SkyCoord(ra=pointings['RA']*u.hour, dec=pointings['DEC']*u.deg, frame='icrs')

        # observing_location = EarthLocation(lat='31d57.5m', lon='-111d35.8m', height=2096*u.m)  # Kitt Peak, Arizona
        # If you're using astropy v1.1 or later, you can replace the above with this:
        observing_location = EarthLocation.of_site('Kitt Peak')
        observing_time = Time('2010-08-21')  # 1am UTC=6pm AZ mountain time
        visibles = self.select_exposures(
            coords, observing_time, observing_location, 87*u.deg)

        return file_html(self.footprint(coords, visibles), CDN, "DESI Footprint")
