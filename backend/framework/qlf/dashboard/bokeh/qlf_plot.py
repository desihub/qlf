import os
import logging
import pandas as pd
import requests
from furl import furl
from bokeh.plotting import Figure


def plot_hist(hover,yrange, yscale="auto", pw=700, ph=400):
    """
    Defaults for histograms
    """
    if yscale not in ["log","auto"]:
        logger.warn('Wrong yscale')
        
    plot = Figure(tools=[hover,"pan,wheel_zoom,box_zoom,reset, crosshair, tap"] 
            , plot_width=pw, plot_height=ph, background_fill_color="white"
            , x_axis_type="auto", y_axis_type=yscale
            , y_range =yrange)

    #plot.add_tools(hover)
    
    return plot

