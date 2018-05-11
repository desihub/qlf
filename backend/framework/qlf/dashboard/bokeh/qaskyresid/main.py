import sys

from bokeh.plotting import Figure
from bokeh.layouts import row, column, widgetbox, gridplot

from bokeh.models.widgets import PreText, Div
from bokeh.models import PrintfTickFormatter
from dashboard.bokeh.helper import write_info, get_scalar_metrics


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

logger = logging.getLogger(__name__)

# =============================================
# THIS comes from INTERFACE
#
args = get_url_args(curdoc)

try:
    selected_process_id = args['process_id']
    selected_arm = args['arm']
    selected_spectrograph = args['spectrograph']
except:
    sys.exit('Invalid args')

# ============================================
#  THIS READ yaml files
#

cam = selected_arm+str(selected_spectrograph)
try:
    lm = get_scalar_metrics(selected_process_id, cam)
    metrics, tests = lm['results']['metrics'], lm['results']['tests']
except:
    sys.exit('Could not load metrics')

skyresid  = metrics['skyresid']
par = tests['skyresid']

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
            x_axis_label='Angstrom',
            plot_width = 720, plot_height = 240,
          tools=[skr_hover,"pan,box_zoom,reset,crosshair, lasso_select" ])

p1.line('wl', 'med_resid', source=skyres_source)

p2 = Figure(title= 'WAVG_RESID_WAVE', 
            x_axis_label='Angstrom',
            plot_width = 720, plot_height = 240,
          tools=[wavg_hover,"pan,box_zoom,reset,crosshair, lasso_select" ])

p2.line('wl', 'wavg_resid', source=skyres_source)


'''p1.circle('wl', 'med_resid', source=skyres_source, alpha = 0, size=1,
          hover_alpha=1,
         hover_fill_color='orange', hover_line_color='red') '''

'''p2.circle('wl', 'wavg_resid', source=skyres_source, alpha=0, size=1,
         hover_alpha=1,
          hover_fill_color='orange', hover_line_color='red')''' 

p1.x_range = p2.x_range

#-------------------------------------
# histogram

xhistlabel= ""
yscale = "auto"#"auto" or "log"

#plotar tambem a mediana do residuo med_resid
#resid normal and warn ranges


hist_tooltip_x = """
    <div>
        <div>
            <span style="font-size: 12px; font-weight: bold; color: #303030;">Frequency: </span>
            <span style="font-size: 13px; color: #515151">@hist</span>
        </div>
        <div>
            <span style="font-size: 12px; font-weight: bold; color: #303030;">XSIGMA: </span>
            <span style="font-size: 13px; color: #515151;">[@left, @right]</span>
        </div>
    </div>
"""

hist, edges  = skyresid['DEVS_1D'], skyresid['DEVS_EDGES']

source_hist = ColumnDataSource(data={
    'hist': hist,
    'histplusone':np.array(hist)+1,
    'bottom':[0] *len(hist),
    'bottomplusone':[1]*len(hist),
    'left':edges[:-1],
    'right':edges[1:]
})

hover = HoverTool(tooltips=hist_tooltip_x)

ylabel,yrange,bottomval,histval = 'Frequency', (0, 1.1*max(hist)), 'bottom','hist'#histpar(yscale, hist)

xhistlabel = "Residuals"
p_hist = Figure(title='',tools=[hover,"pan,wheel_zoom,box_zoom,reset"],
           y_axis_label=ylabel, x_axis_label=xhistlabel, background_fill_color="white"
        , plot_width=700, plot_height=400
        , x_axis_type="auto",    y_axis_type=yscale
        , y_range=yrange)#, y_range=(1, 11**(int(np.log10(max(hist)))+1) ) )

p_hist.quad(top=histval, bottom=bottomval, left='left', right='right',
       source=source_hist, 
        fill_color="dodgerblue", line_color="blue", alpha=0.8,
       hover_fill_color='blue', hover_line_color='black', hover_alpha=0.8)

# Visual alert ranges
logger.info(par['RESID_NORMAL_RANGE'])

for ialert in par['RESID_NORMAL_RANGE']:
    spans = Span(location= ialert , dimension='height', line_color='green',
                          line_dash='dashed', line_width=2)
    p_hist.add_layout(spans)
    my_label = Label(x=ialert, y=yrange[-1]/2.2, y_units='data', text='Normal Range', text_color='green', angle=np.pi/2.)
    p_hist.add_layout(my_label)

for ialert in par['RESID_WARN_RANGE']:
    spans = Span(location= ialert , dimension='height', line_color='tomato',
                          line_dash='dotdash', line_width=2)
    p_hist.add_layout(spans)
    my_label = Label(x=ialert, y=yrange[-1]/2.2, y_units='data', text='Warning Range', text_color='tomato', angle=np.pi/2.)
    p_hist.add_layout(my_label)

residmed = skyresid['MED_RESID']
medianline = Span(location= residmed, dimension='height', line_color='black', line_dash='solid', line_width=2)
p_hist.add_layout(medianline)
my_label = Label(x=residmed, y=0.94*yrange[-1], y_units='data', text='Median', text_color='black', angle=0.
                ,background_fill_color='white', text_align="center",background_fill_alpha=.8)
p_hist.add_layout(my_label)

# --------------------------------------

txt = Div(text="""<table style="text-align:center;font-size:16px;"><tr>
                            <td>{:>40}</td><td>{:<6.5f}</td>
                        </tr>
                        <tr><td>{:>40}</td><td> {:}</td>
                        </tr>
                        <tr><td>{:>40}</td><td> {:}</td>
                        </tr></table>"""
        .format("Median of Residuals:", residmed
                ,"Residuals Normal Range:",par['RESID_NORMAL_RANGE']
                , "Residuals Warning Range:",par['RESID_WARN_RANGE'])
        , width=p2.plot_width)
info, nlines = write_info('skyresid', tests['skyresid'])

#txt = PreText(text=info, height=nlines*20, width=p2.plot_width)
info_col=Div(text=write_description('skyresid'), width=p2.plot_width)
p2txt = column(widgetbox(info_col), p1, p2, widgetbox(txt), p_hist)

#layout=column(p1,p2)
curdoc().add_root(p2txt)
curdoc().title = "SKYRESID"
