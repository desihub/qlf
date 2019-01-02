import os
import logging
import pandas as pd
import requests
from furl import furl
from bokeh.plotting import Figure
from bokeh.models import HoverTool, ColumnDataSource, PrintfTickFormatter
from scalar_metrics import LoadMetrics
import numpy as np


def sort_obj(gen_info):
    """ Hover info of objects type in fibers (wedge) plots.
            input: gen_info= mergedqa['GENERAL_INFO']
            returns: list(500)
    """
    obj_type = ['']*500
    for key in ['LRG', 'ELG', 'QSO', 'STAR', 'SKY']:
        if gen_info.get(key+'_FIBERID', None):
            for i in gen_info[key+'_FIBERID']:
                obj_type[i] = key
        else:
            pass
    return obj_type

def plot_hist(hover, yrange, yscale="auto", pw=600, ph=400):
    """
    Defaults for histograms
    """
    if yscale not in ["log", "auto"]:
        logger.warn('Wrong yscale')
    if yrange == None:
        plot = Figure(tools=[hover, "pan,wheel_zoom,box_zoom,reset, crosshair, tap"], plot_width=pw, active_drag="box_zoom",
                      plot_height=ph, background_fill_color="white", x_axis_type="auto", y_axis_type=yscale)

    else:
        plot = Figure(tools=[hover, "pan,wheel_zoom,box_zoom,reset, crosshair, tap"], plot_width=pw, active_drag="box_zoom",
                      plot_height=ph, background_fill_color="white", x_axis_type="auto", y_axis_type=yscale, y_range=yrange)

    # plot.add_tools(hover)

    return plot


def set_amp(z_value):
    ''' Setup for AMP plots
    '''
    import numpy as np
    dz=z_value

    # removing NaN in ranges
    dz_valid=[ x if x > -999 else np.nan for x in dz ]
    dzmax, dzmin = np.nanmax(dz_valid), np.nanmin(dz_valid) 

    if np.log10(dzmax) > 4 or np.log10(dzmin) <-3:
        ztext = ['{:4.2e}'.format(i) for i in dz_valid]
        cbarformat = "%2.1e"
    elif np.log10(dzmin)>0:
        ztext = ['{:5.2f}'.format(i) for i in dz_valid]
        cbarformat = "%4.2f"
    else:
        ztext = ['{:6.2f}'.format(i) for i in dz_valid]
        cbarformat = "%5.2f"

    return ztext, cbarformat


def plot_amp(dz, refexp, mapper, name="", font_size="1.2vw"):
    ''' Initializing AMP plot
    '''
    ztext, cbarformat = set_amp(dz)
    dx = [0, 1, 0, 1]
    dy = [1, 1, 0, 0]

    cmap_tooltip = """
        <div>

            <div>
                <span style="font-size: 1vw; font-weight: bold; color: #303030;">AMP: </span>
                <span style="font-size: 1vw; color: #515151;">@amp_number</span>
            </div>
            <div>
                <span style="font-size: 1vw; font-weight: bold; color: #303030;">counts: </span>
                <span style="font-size: 1vw; color: #515151">@ztext</span>
            </div>
            <div>
                <span style="font-size: 1vw; font-weight: bold; color: #303030;">Reference: </span>
                <span style="font-size: 1vw; color: #515151;">@ref</span>
            </div>
         </div>
    """.replace("counts:", name.replace("_AMP","")+":")
    hover = HoverTool(tooltips=cmap_tooltip)

    p = Figure(title=name, tools=[hover],
               x_range=list([-0.5, 1.5]),
               y_range=list([-0.5, 1.5]),
               plot_width=450, plot_height=400)


    p.xaxis.axis_label_text_font_size = font_size
    p.legend.label_text_font_size = font_size
    p.title.text_font_size = font_size

    p.grid.grid_line_color = None
    p.outline_line_color = None
    p.axis.clear
    p.axis.minor_tick_line_color = None

    p.axis.major_label_text_font_size = '0pt'
    p.yaxis.major_label_text_font_size = '0pt'
    #p.xaxis.axis_label_text_font_size = "0pt"
    p.xaxis.major_tick_line_color = None
    p.xaxis.minor_tick_line_color = None
    p.yaxis.major_tick_line_color = None
    p.yaxis.minor_tick_line_color = None
    p.yaxis.visible = False
    p.xaxis.visible = True



    zvalid=[x if x>-999 else np.nan for x in dz]
    source = ColumnDataSource(
        data=dict(
            x = dx,
            y = dy,
            z = dz,
            zvalid = zvalid,
            ref=["{:.2f}".format(x) for x in refexp],
            zdiff = np.array(zvalid) -np.array(refexp),
            y_offset1 = [i+0.15 for i in dy],
            y_offset2 = [i-0.10 for i in dy],
            amp = ['AMP %s'%i for i in range(1,5) ] ,
            amp_number = ['%s'%i for i in range(1,5) ] ,
            ztext = ztext,
            )
        )

    text_props = {
        "source": source,
        "angle": 0,
        "color": "black",
        "text_color": "black",
        "text_align": "center",
        "text_baseline": "middle"}

    p.rect("x", "y", .98, .98, 0, source=source,
           fill_color={'field': 'zdiff', 'transform': mapper}, fill_alpha=0.9)

    p.text(x="x", y="y_offset1", text="amp",
            text_font_size="2vw", **text_props)
    p.text(x="x", y="y_offset2", text="ztext",
           text_font_style="bold", text_font_size="2.5vw", **text_props)
    

    return p


if __name__ == '__main__':
    logger.info('Standalone execution')
