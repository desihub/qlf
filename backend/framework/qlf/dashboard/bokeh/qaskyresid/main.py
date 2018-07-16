import sys

from bokeh.plotting import Figure
from bokeh.layouts import row, column, widgetbox, gridplot

from bokeh.models.widgets import PreText, Div
from bokeh.models import PrintfTickFormatter
from dashboard.bokeh.helper import write_info, get_scalar_metrics

from dashboard.bokeh.qlf_plot import html_table
from bokeh.io import curdoc
from bokeh.io import output_notebook, show, output_file

from bokeh.models import Span, Label
from bokeh.models import ColumnDataSource, HoverTool, TapTool, Range1d, OpenURL
from bokeh.models import LinearColorMapper, ColorBar
from bokeh.models.widgets import Select, Slider
from dashboard.bokeh.helper import get_url_args, write_description, \
    get_scalar_metrics

import numpy as np
import logging
from bokeh.resources import CDN
from bokeh.embed import file_html
logger = logging.getLogger(__name__)


class Skyresid:
    def __init__(self, process_id, arm, spectrograph):
            self.selected_process_id = process_id
            self.selected_arm = arm
            self.selected_spectrograph = spectrograph

    def load_qa(self):
        cam = self.selected_arm+str(self.selected_spectrograph)
        try:
            lm = get_scalar_metrics(self.selected_process_id, cam)
            metrics, tests = lm['metrics'], lm['tests']
        except:
            sys.exit('Could not load metrics')

        skyresid  = metrics['skyresid']
        par = tests['skyresid']

        residmed = skyresid['MED_RESID']

        # ============================================
        # THIS: Given the set up in the block above, 
        #       we have the bokeh plots

        skr_tooltip = """
            <div>
                <div>
                    <span style="font-size: 12px; font-weight: bold; color: #303030;">Wavelength: </span>
                    <span style="font-size: 13px; color: #515151">@wl &#8491</span>
                </div>
                <div>
                    <span style="font-size: 12px; font-weight: bold; color: #303030;">y: </span>
                    <span style="font-size: 13px; color: #515151;">@med_resid</span>
                </div>
            </div>
        """

        wavg_tooltip = """
            <div>
                <div>
                    <span style="font-size: 12px; font-weight: bold; color: #303030;">Wavelength: </span>
                    <span style="font-size: 13px; color: #515151">@wl &#8491</span>
                </div>
                <div>
                    <span style="font-size: 12px; font-weight: bold; color: #303030;">y: </span>
                    <span style="font-size: 13px; color: #515151;">@wavg_resid</span>
                </div>
            </div>
        """

        skr_hover=HoverTool(tooltips=skr_tooltip, mode='vline')
        wavg_hover=HoverTool(tooltips=wavg_tooltip, mode='vline')


        skyres_source = ColumnDataSource(
                        data={'wl': skyresid['WAVELENGTH'],
                            'med_resid' : skyresid['MED_RESID_WAVE'],
                            'wavg_resid':  skyresid['WAVG_RES_WAVE']
                            })

        p1 = Figure(title= 'MED_RESID_WAVE', 
                    x_axis_label='Wavelength (A)', y_axis_label='Counts',
                    plot_width = 500, plot_height = 240,
                tools=[skr_hover,"pan,box_zoom,reset,crosshair, lasso_select" ])

        p1.line('wl', 'med_resid', source=skyres_source)

        p2 = Figure(title= 'WAVG_RESID_WAVE', 
                    x_axis_label='Wavelength (A)', y_axis_label='Counts',
                    plot_width = 500, plot_height = 240,
                tools=[wavg_hover,"pan,box_zoom,reset,crosshair, lasso_select" ])

        p2.line('wl', 'wavg_resid', source=skyres_source)


        '''p1.circle('wl', 'med_resid', source=skyres_source, alpha = 0, size=1,
                hover_alpha=1,
                hover_fill_color='orange', hover_line_color='red') '''

        '''p2.circle('wl', 'wavg_resid', source=skyres_source, alpha=0, size=1,
                hover_alpha=1,
                hover_fill_color='orange', hover_line_color='red')''' 

        p1.x_range = p2.x_range


        #--------------
        # hist fiber
        from dashboard.bokeh.qlf_plot import plot_hist
        hist_tooltip=""" 
            <div>
                <div>
                    <span style="font-size: 12px; font-weight: bold; color: #303030;">MEDIAN RESID: </span>
                    <span style="font-size: 13px; color: #515151;">@median_resid</span>
                </div>
                <div>
                    <span style="font-size: 12px; font-weight: bold; color: #303030;">FIBER ID: </span>
                    <span style="font-size: 13px; color: #515151;">@fiberid</span>
                </div>
            </div>
                """
        hist_hover = HoverTool(tooltips=hist_tooltip)
        hist_source = ColumnDataSource(
                        data={'median_resid': skyresid['MED_RESID_FIBER'],
                            'fiberid' : skyresid['SKYFIBERID'],#[str(i) for i in skyresid['SKYFIBERID'] ],
                            'x': np.arange(len(skyresid['SKYFIBERID'])),
                            'left': np.arange(len(skyresid['SKYFIBERID'])) -0.4,
                            'right':np.arange(len(skyresid['SKYFIBERID']))+0.4,
                            'bottom':[0]*len(skyresid['SKYFIBERID']),
                            })

        #yrange=[0, max(skyresid['MED_RESID_FIBER']) *1.1]
        fiber_hist = plot_hist(hist_hover,None, ph=300, pw=450)

        fiber_hist.vbar(top='median_resid', x='x', width=0.8,
                    source=hist_source,
                    fill_color="dodgerblue", line_color="black", line_width =0.01, alpha=0.8,
                    hover_fill_color='red', hover_line_color='red', hover_alpha=0.8)
        fiber_hist.xaxis.axis_label="Fiber number"
        fiber_hist.yaxis.axis_label="Median resid."

        strx=[str(i) for i in range(len(skyresid['SKYFIBERID']))]
        strf=[str(i) for i in skyresid['SKYFIBERID'] ]
        fiber_hist.xaxis.major_label_overrides = dict(zip(strx,strf))

        text2=""""""
        for i in ['NBAD_PCHI','NREJ','NSKY_FIB','RESID_PER']:      
            text2=text2+ ("""<tr>
                            <td>{:>40}:</td> <td style='text-align:left'>{:}</td>
                            </tr> """.format(i,skyresid[i]))

        txt = Div(text="""<table style="text-align:right;font-size:16px;">
                                <tr>
                                    <td>{:>40}:</td><td style='text-align:left'>{:}</td>
                                </tr>
                                {}
                                <tr>
                                    <td>{:>40}:</td><td style='text-align:left'> {:}</td>
                                </tr>
                                <tr>
                                    <td>{:>40}:</td><td style='text-align:left'> {:}</td>
                                </tr>
                        </table>"""
                .format("Median of Residuals:", residmed
                        ,text2
                        ,"Residuals Normal Range",par['RESID_NORMAL_RANGE']
                        , "Residuals Warning Range",par['RESID_WARN_RANGE'])
                , width=p2.plot_width)
        info, nlines = write_info('skyresid', tests['skyresid'])


        info_col=Div(text=write_description('skyresid'), width=p2.plot_width)

        resid_vals=[]
        resid_names=[]
        for i in ['MED_RESID','NREJ','NSKY_FIB']:#,'RESID_PER']:
            resid_names.append(i)
            if i == 'RESID_PER': #95% c.l. boundaries of residuals distribution
                resid_vals.append('[{:.3f}, {:.3f}]'.format(skyresid[i][0], skyresid[i][1])) 
            elif isinstance(skyresid[i], float):
                resid_vals.append('{:.3f}'.format(skyresid[i])  )
            else:
                resid_vals.append(skyresid[i]) 
        
        resid_names=['Median of Residuals (sky fibers)', 'Number of reject fibers', 'Number of good sky fibers'] 
        nrg= tests['skyresid']['RESID_NORMAL_RANGE']
        wrg= tests['skyresid']['RESID_WARN_RANGE']
        tb = html_table(names=resid_names, vals=resid_vals, nrng=nrg, wrng=wrg  )
        tbinfo=Div(text=tb, width=400)


        # p2txt = column(widgetbox(info_col), row(column(p1, p2), tbinfo), fiber_hist  )
        layout = column(widgetbox(info_col, css_classes=["header"]),
                      widgetbox(tbinfo, css_classes=["table-ranges"]),
                      p1,
                      fiber_hist,
                      p2,
                      css_classes=["display-grid-skyresid"])
        return file_html(layout, CDN, "SKYRESID")
