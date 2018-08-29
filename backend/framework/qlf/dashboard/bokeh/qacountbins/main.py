import sys

from bokeh.plotting import Figure
from bokeh.layouts import row, column, widgetbox, gridplot

from bokeh.models import HoverTool, ColumnDataSource, Range1d, Label, FixedTicker
from bokeh.models import (LinearColorMapper ,    ColorBar)


from bokeh.palettes import (RdYlBu, Colorblind, Viridis256)

import numpy as np

from dashboard.bokeh.helper import get_url_args, write_description,\
    get_merged_qa_scalar_metrics
from dashboard.bokeh.qlf_plot import plot_hist, html_table, sort_obj

import numpy as np
import logging
from bokeh.resources import CDN
from bokeh.embed import file_html
#Additional imports:
from bokeh.models.widgets import Div


logger = logging.getLogger(__name__)


class Countbins:
    def __init__(self, process_id, arm, spectrograph):
            self.selected_process_id = process_id
            self.selected_arm = arm
            self.selected_spectrograph = spectrograph

    def load_qa(self):
        cam = self.selected_arm+str(self.selected_spectrograph)

        try:
            mergedqa = get_merged_qa_scalar_metrics(self.selected_process_id, cam)
            check_fibers = mergedqa['TASKS']['CHECK_FIBERS']
            gen_info = mergedqa['GENERAL_INFO']

            countbins  = check_fibers['METRICS']
            ra = gen_info['RA']
            dec = gen_info['DEC']
            nrg = check_fibers['PARAMS']['NGOODFIB_NORMAL_RANGE']
            wrg = check_fibers['PARAMS']['NGOODFIB_WARN_RANGE']

        except Exception as err:
            logger.info(err)
            sys.exit('Could not load data')




        qlf_fiberid = np.arange(0, 500) # the fiber id is giving by petal

        obj_type = sort_obj(mergedqa['GENERAL_INFO'])


        hist_tooltip=""" 
            <div>
                <div>
                    <span style="font-size: 12px; font-weight: bold; color: #303030;">FIBER STATUS: </span>
                    <span style="font-size: 13px; color: #515151;">@status</span>
                </div>
                <div>
                    <span style="font-size: 12px; font-weight: bold; color: #303030;">FIBER ID: </span>
                    <span style="font-size: 13px; color: #515151;">@fiberid</span>
                </div>
            </div>
                """
        y=np.array(countbins['GOOD_FIBER'])
        x=np.array(range(len(countbins['GOOD_FIBER'])))
        hist_hover = HoverTool(tooltips=hist_tooltip)
        hist_source = ColumnDataSource(
                        data={'goodfiber': y,
                            'fiberid' : x,
                                'segx0': x -0.4,
                                'segx1': x +0.4,
                                'segy0': y ,
                                'segy1': y ,
                                'status': ['GOOD' if i==1 else 'BAD' for i in y],
                                'x1': ra,
                                'y1': dec,   
                            'QLF_FIBERID': qlf_fiberid,
                            'OBJ_TYPE': obj_type,
                            'color': ['#319b5c' if i ==1 else '#282828' for i in countbins['GOOD_FIBER']]
                            })


        p = Figure(tools = [hist_hover,"pan,wheel_zoom,  box_zoom, lasso_select, reset, crosshair, tap"],
                    plot_width=550, plot_height=300, y_range = Range1d(-.1,1.1),
                    x_axis_label='Fiber', y_axis_label=' Fiber Status'
                    )
        from bokeh.models.glyphs import Segment

        seg=Segment(x0='segx0', x1='segx1', y0='segy0',y1='segy1', line_width=2, line_color='#1e90ff')

        p.add_glyph(hist_source, seg)
        label = Label(x=330, y=0.7, x_units='data', y_units='data',
                        text='NGOOD_FIBER: {}'.format(countbins['NGOODFIB']), render_mode='css',
                        border_line_color='black', border_line_alpha=1.0,
                        background_fill_color='white', background_fill_alpha=1.0)

        p.yaxis.ticker=FixedTicker(ticks=[0,1])
        p.yaxis.major_label_overrides = {'0':'bad', '1':'good'}
        p.add_layout(label)


        #----------------
        # Wedge
        count_tooltip = """
            <div>
                <div>
                    <span style="font-size: 12px; font-weight: bold; color: #303030;">FIBER STATUS: </span>
                    <span style="font-size: 13px; color: #515151">@status</span>
                </div>
                <div>
                    <span style="font-size: 12px; font-weight: bold; color: #303030;">RA: </span>
                    <span style="font-size: 13px; color: #515151;">@x1</span>
                </div>
                <div>
                    <span style="font-size: 12px; font-weight: bold; color: #303030;">DEC: </span>
                    <span style="font-size: 13px; color: #515151;">@y1</span>
                </div>
                <div>
                    <span style="font-size: 12px; font-weight: bold; color: #303030;">Obj Type: </span>
                    <span style="font-size: 13px; color: #515151;">@OBJ_TYPE</span>
                </div>
            </div>
        """



        hover = HoverTool(tooltips=count_tooltip)


        radius = 0.013
        radius_hover = 0.015

        # axes limit
        xmin, xmax = [min(ra), max(ra)]
        ymin, ymax = [min(dec), max(dec)]
        xfac, yfac  = [(xmax-xmin)*0.06, (ymax-ymin)*0.06]
        left, right = xmin -xfac, xmax+xfac
        bottom, top = ymin-yfac, ymax+yfac

        

        p2 = Figure(title= 'GOOD FIBERS'
                , x_axis_label='RA', y_axis_label='DEC'
                , plot_width=400, plot_height=400
                , tools=[hover, "pan,box_zoom,reset,lasso_select,crosshair, tap"]
                , toolbar_location="right"
                )

        # Color Map
        p2.circle('x1', 'y1', source=hist_source, name="data", radius=radius,
                fill_color= {'field':'color'}, 
                line_color='black', line_width=0.3,
                hover_line_color='red')

        # marking the Hover point
        p2.circle('x1', 'y1', source=hist_source, name="data", radius=radius_hover, 
                  hover_fill_color={'field': 'color'}, fill_color=None,
                  line_color=None, line_width=3, hover_line_color='red')

        ngood = countbins['NGOODFIB']
        fracgood= ngood/500. -1.
        tb = html_table(names=['NGOODFIB', 'FRACTION BAD'], vals=[ngood, str(fracgood*100)+' %' ],
                        nrng=nrg, wrng=wrg  )
        tbinfo = Div(text=tb, width=400)

        info_col = Div(text=write_description('countbins'))

        layout = column(widgetbox(info_col, css_classes=["header"]),
                      widgetbox(tbinfo, css_classes=["table-ranges"]),
                      p,
                      p2,
                      css_classes=["display-grid-countbins"])

        return file_html(layout, CDN, "COUNTBINS")
