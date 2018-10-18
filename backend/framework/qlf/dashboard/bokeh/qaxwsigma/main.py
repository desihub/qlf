from bokeh.plotting import figure
from bokeh.layouts import column, widgetbox, gridplot

from bokeh.models import Span, Label

from bokeh.models import ColumnDataSource, HoverTool, Range1d, OpenURL
from bokeh.models import LinearColorMapper, ColorBar
from dashboard.bokeh.helper import write_description, get_merged_qa_scalar_metrics
from dashboard.bokeh.qlf_plot import plot_hist, sort_obj
from dashboard.bokeh.qlf_plot import metric_table, alert_table
from bokeh.models import TapTool, OpenURL
from bokeh.models.widgets import Div
from bokeh.resources import CDN
from bokeh.embed import file_html
import numpy as np
import logging
from dashboard.bokeh.helper import get_palette
from dashboard.bokeh.qlf_plot import set_amp, plot_amp
from bokeh.models import PrintfTickFormatter


class Xwsigma:
    def __init__(self, process_id, arm, spectrograph):
        self.selected_process_id = process_id
        self.selected_arm = arm
        self.selected_spectrograph = spectrograph

    def load_qa(self):

        cam = self.selected_arm+str(self.selected_spectrograph)

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

        handler = logging.FileHandler("logs/bokeh_qlf.log")
        handler.setLevel(logging.INFO)
        logger.addHandler(handler)

        mergedqa = get_merged_qa_scalar_metrics(self.selected_process_id, cam)

        gen_info = mergedqa['GENERAL_INFO']

        ra = gen_info['RA']
        dec = gen_info['DEC']

        check_ccds = mergedqa['TASKS']['CHECK_CCDs']

        xwsigma = check_ccds['METRICS']['XWSIGMA']
        xw_amp = check_ccds['METRICS']['XWSIGMA_AMP']

        xw_fib = check_ccds['METRICS']['XWSIGMA_FIB']

        nrg = check_ccds['PARAMS']['XWSIGMA_NORMAL_RANGE']
        wrg = check_ccds['PARAMS']['XWSIGMA_WARN_RANGE']
        xw_ref = check_ccds['PARAMS']['XWSIGMA_REF']

        xsigma = xw_fib[0]
        wsigma = xw_fib[1]

        delta_rg = wrg[1] - wrg[0]
        hist_rg = (wrg[0] - 0.1*delta_rg, wrg[1]+0.1*delta_rg)

        my_palette = get_palette("viridis")

        xsigma_tooltip = """
            <div>
                <div>
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">XSigma: </span>
                    <span style="font-size: 1vw; color: #515151">@xsigma</span>
                </div>
                <div>
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">Obj Type: </span>
                    <span style="font-size: 1vw; color: #515151;">@OBJ_TYPE</span>
                </div>
                <div>
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">RA: </span>
                    <span style="font-size: 1vw; color: #515151;">@x1</span>
                </div>
                <div>
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">DEC: </span>
                    <span style="font-size: 1vw; color: #515151;">@y1</span>
                </div>

                <div>
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">FIBER #: </span>
                    <span style="font-size: 1vw; color: #515151;">@xfiber</span>
                </div>

            </div>
        """

        wsigma_tooltip = """
            <div>
                <div>
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">WSigma: </span>
                    <span style="font-size: 1vw; color: #515151">@wsigma</span>
                </div>
                <div>
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">Obj Type: </span>
                    <span style="font-size: 1vw; color: #515151;">@OBJ_TYPE</span>
                </div>
                <div>
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">RA: </span>
                    <span style="font-size: 1vw; color: #515151;">@x1</span>
                </div>
                <div>
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">DEC: </span>
                    <span style="font-size: 1vw; color: #515151;">@y1</span>
                </div>
                <div>
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">FIBER #: </span>
                    <span style="font-size: 1vw; color: #515151;">@wfiber</span>
                </div>

            </div>
        """

        url = "http://legacysurvey.org/viewer?ra=@ra&dec=@dec&zoom=16&layer=decals-dr5"

        # determining the position of selected cam fibers:

        obj_type = sort_obj(gen_info)  # [""]*500
        # ---------------------------------

        xsigma_hover = HoverTool(tooltips=xsigma_tooltip)
        wsigma_hover = HoverTool(tooltips=wsigma_tooltip)

        xfiber = np.arange(len(xsigma))
        wfiber = np.arange(len(wsigma))

        source = ColumnDataSource(data={
            'x1': ra,  # xwsigma['RA'][c1:c2],
            'y1': dec,  # xwsigma['DEC'][c1:c2],
            'xsigma': xsigma,
            'wsigma': wsigma,
            'xfiber': xfiber,
            'wfiber': wfiber,
            'OBJ_TYPE': obj_type,
            'left': np.arange(0, 500)-0.4,
            'right': np.arange(0, 500)+0.4,
            'bottom': [0]*500
        })

        # axes limit
        xmin, xmax = [min(ra[:]), max(ra[:])]
        ymin, ymax = [min(dec[:]), max(dec[:])]
        xfac, yfac = [(xmax-xmin)*0.06, (ymax-ymin)*0.06]
        left, right = xmin - xfac, xmax+xfac
        bottom, top = ymin-yfac, ymax+yfac

        xmapper = LinearColorMapper(palette=my_palette,
                                    low=0.98*np.min(xsigma),
                                    high=1.02*np.max(xsigma))

        wmapper = LinearColorMapper(palette=my_palette,
                                    low=0.99*np.min(wsigma),
                                    high=1.01*np.max(wsigma))

        # ======
        # XSIGMA

        radius = 0.013  # 0.015
        radius_hover = 0.015  # 0.0165

        px = figure(title='XSIGMA',
            x_axis_label='RA',
            y_axis_label='DEC',
            plot_height=350,
            x_range=Range1d(left,right),
            y_range=Range1d(bottom,
            top),
            tools=[xsigma_hover,
            "box_zoom,pan,reset,crosshair"],
            active_drag="box_zoom")

        # Color Map
        px.circle('x1','y1', source=source, name="data", radius=radius,
                  fill_color={'field': 'xsigma', 'transform': xmapper},
                  line_color='black', line_width=0.1,
                  hover_line_color='red')

        # marking the Hover point
        px.circle('x1', 'y1', source=source, name="data", radius=radius_hover, hover_fill_color={
                  'field': 'xsigma', 'transform': xmapper}, fill_color=None, line_color=None, line_width=3, hover_line_color='red')

        taptool = px.select(type=TapTool)
        taptool.callback = OpenURL(url=url)

        xcolor_bar = ColorBar(color_mapper=xmapper, label_standoff=-13,
                              major_label_text_font_style="bold", padding=26,
                              major_label_text_align='right',
                              major_label_text_font_size="10pt",
                              location=(0, 0))

        px.add_layout(xcolor_bar, 'left')

        # x_fiber_hist
        d_yplt = (max(xsigma) - min(xsigma))*0.1
        yrange = [0, max(xsigma) + d_yplt]

        xhist = plot_hist(xsigma_hover, yrange, ph=300)
        xhist.quad(top='xsigma', bottom='bottom', left='left', right='right', name='data', source=source,
                   fill_color="dodgerblue", line_color="black", line_width=0.01, alpha=0.8,
                   hover_fill_color='red', hover_line_color='red', hover_alpha=0.8)

        xhist.xaxis.axis_label = "Fiber number"
        xhist.yaxis.axis_label = "X std dev (number of pixels)"

        # ======
        # WSIGMA
        pw = figure(title='WSIGMA',
                x_axis_label='RA',
                y_axis_label='DEC',
                plot_height=350,
                x_range=Range1d(left,right),
                y_range=Range1d(bottom,top),
                tools=[wsigma_hover,
                "box_zoom,pan,reset,crosshair"],
                active_drag="box_zoom")

        # Color Map
        pw.circle('x1','y1', source=source, name="data", radius=radius,
                  fill_color={'field': 'wsigma', 'transform': wmapper},
                  line_color='black', line_width=0.1,
                  hover_line_color='red')

        # marking the Hover point
        pw.circle('x1', 'y1', source=source, name="data", radius=radius_hover, hover_fill_color={
                  'field': 'wsigma', 'transform': wmapper}, fill_color=None, line_color=None, line_width=3, hover_line_color='red')

        taptool = pw.select(type=TapTool)
        taptool.callback = OpenURL(url=url)

        wcolor_bar = ColorBar(color_mapper=wmapper, label_standoff=-13,
                              major_label_text_font_style="bold", padding=26,
                              major_label_text_align='right',
                              major_label_text_font_size="10pt",
                              location=(0, 0))

        pw.add_layout(wcolor_bar, 'left')

        # w_fiber_hist
        d_yplt = (max(wsigma) - min(wsigma))*0.1
        yrange = [0, max(wsigma) + d_yplt]

        whist = plot_hist(wsigma_hover, yrange, ph=300)
        whist.quad(top='wsigma', bottom='bottom', left='left', right='right', name='data', source=source,
                   fill_color="dodgerblue", line_color="black", line_width=0.01, alpha=0.8,
                   hover_fill_color='red', hover_line_color='red', hover_alpha=0.8)
        whist.xaxis.axis_label = "Fiber number"
        whist.yaxis.axis_label = "W std dev (number of pixels)"

        # ================================
        # Stat histogram

        def histpar(yscale, hist):
            if yscale == 'log':
                ylabel = "Frequency + 1"
                yrange = (1, 11**(int(np.log10(max(hist)))+1))
                bottomval = 'bottomplusone'
                histval = 'histplusone'
            else:
                ylabel = "Frequency"
                yrange = (-0.1*max(hist), 1.1*max(hist))
                bottomval = 'bottom'
                histval = 'hist'
            return [ylabel, yrange, bottomval, histval]

        yrangex = yrange

        xhistlabel = "XSIGMA"
        yscale = "auto"

        hist_tooltip_x = """
            <div>
                <div>
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">Frequency: </span>
                    <span style="font-size: 1vw; color: #515151">@hist</span>
                </div>
                <div>
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">XSIGMA: </span>
                    <span style="font-size: 1vw; color: #515151;">[@left, @right]</span>
                </div>
            </div>
        """

        hist, edges = np.histogram(xsigma, 'sqrt')

        source_hist = ColumnDataSource(data={
            'hist': hist,
            'histplusone': hist+1,
            'bottom': [0] * len(hist),
            'bottomplusone': [1]*len(hist),
            'left': edges[:-1],
            'right': edges[1:]
        })

        hover = HoverTool(tooltips=hist_tooltip_x)

        ylabel, yrange, bottomval, histval = histpar(yscale, hist)

        p_hist_x = figure(sizing_mode='scale_width', title='', tools=[hover, "box_zoom,wheel_zoom,pan,reset"], active_drag="box_zoom", plot_height=300,
                          y_axis_label=ylabel, x_axis_label=xhistlabel, background_fill_color="white", x_axis_type="auto", y_axis_type=yscale, y_range=yrange, x_range=hist_rg
                          )

        p_hist_x.quad(top=histval, bottom=bottomval, left='left', right='right',
                      source=source_hist,
                      fill_color="dodgerblue", line_color='blue', alpha=0.8,
                      hover_fill_color='blue', hover_line_color='black', hover_alpha=0.8)

        p_hist_x.xaxis.visible = True

        # Histogram 2
        xhistlabel = "WSIGMA"
        hist_tooltip_w = """
            <div>
                <div>
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">Frequency: </span>
                    <span style="font-size: 1vw; color: #515151">@hist</span>
                </div>
                <div>
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">WSIGMA: </span>
                    <span style="font-size: 1vw; color: #515151;">[@left, @right]</span>
                </div>
            </div>
        """

        hist, edges = np.histogram(wsigma, 'sqrt')

        source_hist = ColumnDataSource(data={
            'hist': hist,
            'histplusone': hist+1,
            'bottom': [0] * len(hist),
            'bottomplusone': [1]*len(hist),
            'left': edges[:-1],
            'right': edges[1:]
        })

        hover = HoverTool(tooltips=hist_tooltip_w)

        ylabel, yrange, bottomval, histval = histpar(yscale, hist)
        yrangew = yrange

        p_hist_w = figure(sizing_mode='scale_width', title='', tools=[hover, "box_zoom, pan,wheel_zoom,reset"], active_drag="box_zoom",
                          y_axis_label=ylabel, x_axis_label=xhistlabel, background_fill_color="white", plot_height=300, x_axis_type="auto",    y_axis_type=yscale, y_range=yrange, x_range=hist_rg)  # , y_range=(1, 11**(int(np.log10(max(hist)))+1) ) )

        p_hist_w.quad(top=histval, bottom=bottomval, left='left', right='right',
                      source=source_hist,
                      fill_color="dodgerblue", line_color='blue', alpha=0.8,
                      hover_fill_color='blue', hover_line_color='black', hover_alpha=0.8)

        # --------------------------------------------------------------
        # vlines ranges:
        bname = 'XWSIGMA'

        for ialert in nrg:  # par[bname+'_NORMAL_RANGE']:
            spans = Span(location=ialert, dimension='height', line_color='green',
                         line_dash='dashed', line_width=2)
            p_hist_x.add_layout(spans)
            my_label = Label(x=ialert, y=yrangex[-1]/2.2, y_units='data',
                             text='Normal Range', text_color='green', angle=np.pi/2.)
            p_hist_x.add_layout(my_label)

        for ialert in wrg:  # par[bname+'_WARN_RANGE']:
            spans = Span(location=ialert, dimension='height', line_color='tomato',
                         line_dash='dotdash', line_width=2)
            p_hist_x.add_layout(spans)
            my_label = Label(x=ialert, y=yrangex[-1]/2.2, y_units='data',
                             text='Warning Range', text_color='tomato', angle=np.pi/2.)
            p_hist_x.add_layout(my_label)

        for ialert in nrg:  # par[bname+'_NORMAL_RANGE']:
            spans = Span(location=ialert, dimension='height', line_color='green',
                         line_dash='dashed', line_width=2)
            p_hist_w.add_layout(spans)
            my_label = Label(x=ialert, y=yrangew[-1]/2.2, y_units='data',
                             text='Normal Range', text_color='green', angle=np.pi/2.)
            p_hist_w.add_layout(my_label)

        for ialert in wrg:  # par[bname+'_WARN_RANGE']:
            spans = Span(location=ialert, dimension='height', line_color='tomato',
                         line_dash='dotdash', line_width=2)
            p_hist_w.add_layout(spans)
            my_label = Label(x=ialert, y=yrangew[-1]/2.2, y_units='data',
                             text='Warning Range', text_color='tomato', angle=np.pi/2.)
            p_hist_w.add_layout(my_label)

        dz = xw_amp[0]  # xwsigma['XWSIGMA_AMP'][0]
        name = 'XSIGMA AMP'
        Reds = get_palette('Reds')
        mapper = LinearColorMapper(palette=Reds, low=min(dz), high=max(dz))

        ztext, cbarformat = set_amp(dz)
        xamp = plot_amp(dz, mapper, name=name)

        formatter = PrintfTickFormatter(format=cbarformat)
        color_bar = ColorBar(color_mapper=mapper,  major_label_text_align='left',
                             major_label_text_font_size='10pt', label_standoff=2, location=(0, 0),
                             formatter=formatter, title="", title_text_baseline="alphabetic")
        xamp.height = 400
        xamp.add_layout(color_bar, 'right')

        dz = xw_amp[1]  # xwsigma['XWSIGMA_AMP'][1]
        name = 'WSIGMA AMP'
        Reds = get_palette('Reds')
        mapper = LinearColorMapper(palette=Reds, low=min(dz), high=max(dz))

        ztext, cbarformat = set_amp(dz)
        wamp = plot_amp(dz, mapper, name=name)

        formatter = PrintfTickFormatter(format=cbarformat)
        color_bar = ColorBar(color_mapper=mapper,  major_label_text_align='left',
                             major_label_text_font_size='10pt', label_standoff=2, location=(0, 0),
                             formatter=formatter, title="", title_text_baseline="alphabetic")
        wamp.height = 400
        wamp.add_layout(color_bar, 'right')

        # -------------------------------------------------------------------------
        info_col = Div(text=write_description('xwsigma'))
        pxh = column(px, xhist, p_hist_x, xamp)
        pwh = column(pw, whist, p_hist_w, wamp)

        curexp, refexp = '%3.2f' % xwsigma[0], '%3.2f' % xw_ref[0]  # 'xx..xx'
        info = metric_table('X sigma', 'xsigma', curexp, refexp)
        tb_x = Div(text=info)

        curexp, refexp = '%3.2f' % xwsigma[1], '%3.2f' % xw_ref[1]
        info = metric_table('W sigma', 'wsigma', curexp, refexp)
        tb_w = Div(text=info)

        alert_x = alert_table(nrg, wrg)
        alert_w = alert_table(nrg, wrg)
        tb_alert_x = Div(text=alert_x)
        tb_alert_w = Div(text=alert_w)

        font_size = "1vw"
        for plot in [px, pw, xhist, whist, p_hist_x, p_hist_w, xamp, wamp]:
            plot.xaxis.major_label_text_font_size = font_size
            plot.yaxis.major_label_text_font_size = font_size
            plot.xaxis.axis_label_text_font_size = font_size
            plot.yaxis.axis_label_text_font_size = font_size
            plot.legend.label_text_font_size = font_size
            plot.title.text_font_size = font_size

        layout = column(
            widgetbox(info_col, css_classes=["header"]),
            widgetbox(Div(), css_classes=["tableranges"]),
            widgetbox(tb_x),
            widgetbox(tb_w),
            widgetbox(tb_alert_x),
            widgetbox(tb_alert_w),
            column(px, sizing_mode='scale_both'),
            column(pw, sizing_mode='scale_both'),
            column(xhist, sizing_mode='scale_both'),
            column(whist, sizing_mode='scale_both'),
            column(p_hist_x, sizing_mode='scale_both'),
            column(p_hist_w, sizing_mode='scale_both'),
            column(xamp, sizing_mode='scale_both'),
            column(wamp, sizing_mode='scale_both'),
            css_classes=["display-grid"], sizing_mode='scale_width')
        return file_html(layout, CDN, "XWSIGMA")
