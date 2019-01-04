from bokeh.plotting import Figure
from bokeh.layouts import column, widgetbox, gridplot

from bokeh.models import Span, Label

from bokeh.models import ColumnDataSource, HoverTool, Range1d, OpenURL
from bokeh.models import LinearColorMapper, ColorBar
from dashboard.bokeh.helper import get_merged_qa_scalar_metrics
from dashboard.bokeh.qlf_plot import sort_obj
from bokeh.models import TapTool, OpenURL
from bokeh.models.widgets import Div
from bokeh.resources import CDN
from bokeh.embed import file_html
import numpy as np
import logging
from dashboard.bokeh.helper import get_palette
from bokeh.models import PrintfTickFormatter
from dashboard.bokeh.plots.descriptors.table import Table
from dashboard.bokeh.plots.patch.main import Patch
from dashboard.bokeh.plots.descriptors.title import Title
from dashboard.bokeh.plots.plot2d.main import Plot2d


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
        flavor= mergedqa['FLAVOR']



        ra = gen_info['RA']
        dec = gen_info['DEC']

        check_ccds = mergedqa['TASKS']['CHECK_CCDs']

        xwsigma = check_ccds['METRICS']['XWSIGMA']
        xw_amp = check_ccds['METRICS']['XWSIGMA_AMP']

        xw_fib = check_ccds['METRICS']['XWSIGMA_FIB']

        nrg = check_ccds['PARAMS']['XWSIGMA_NORMAL_RANGE']
        wrg = check_ccds['PARAMS']['XWSIGMA_WARN_RANGE']
        obj_type = sort_obj(gen_info)  # [""]*500

        if mergedqa['FLAVOR'].upper() == 'SCIENCE':
            program = mergedqa['GENERAL_INFO']['PROGRAM'].upper()
            program_prefix = '_'+program
        else:
            program_prefix = ''
        xw_ref = check_ccds['PARAMS']['XWSIGMA'+program_prefix+'_REF']

        xsigma = xw_fib[0]
        wsigma = xw_fib[1]

        delta_rg = wrg[1] - wrg[0]
        hist_rg = (wrg[0] - 0.1*delta_rg, wrg[1]+0.1*delta_rg)

        my_palette = get_palette("viridis")

        xfiber = np.arange(len(xsigma))
        wfiber = np.arange(len(wsigma))
        if mergedqa['FLAVOR'].upper() != 'SCIENCE':
            ra = np.full(500,np.nan)
            dec= np.full(500,np.nan)

        source = ColumnDataSource(data={
            'x1': ra,  
            'y1': dec, 
            'xsigma': xsigma,
            'wsigma': wsigma,
            'xfiber': xfiber,
            'wfiber': wfiber,
            'OBJ_TYPE': obj_type,
            'left': np.arange(0, 500)-0.4,
            'right': np.arange(0, 500)+0.4,
            'bottom': [0]*500
            })


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
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">FIBER ID: </span>
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
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">FIBER ID: </span>
                    <span style="font-size: 1vw; color: #515151;">@wfiber</span>
                </div>

            </div>
            """

        url = "http://legacysurvey.org/viewer?ra=@ra&dec=@dec&zoom=16&layer=decals-dr5"

        # determining the position of selected cam fibers:
        obj_type = sort_obj(gen_info)
        # ---------------------------------

        xsigma_hover = HoverTool(tooltips=xsigma_tooltip)
        wsigma_hover = HoverTool(tooltips=wsigma_tooltip)
        xsigma_std = HoverTool(tooltips=xsigma_tooltip, mode='vline')
        wsigma_std = HoverTool(tooltips=wsigma_tooltip, mode='vline')




        if flavor=="science":
            

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

            # ============
            # XSIGMA WEDGE

            radius = 0.0165 
            radius_hover = 0.02

            # centralize wedges in plots:
            ra_center=0.5*(max(ra)+min(ra))
            dec_center=0.5*(max(dec)+min(dec))
            xrange_wedge = Range1d(start=ra_center + .95, end=ra_center-.95)
            yrange_wedge = Range1d(start=dec_center+.82, end=dec_center-.82)

            px = Figure(title='XSIGMA',
                x_axis_label='RA',
                y_axis_label='DEC',
                plot_height=350,
                x_range=xrange_wedge,
                y_range=yrange_wedge,
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


            # ============
            # WSIGMA WEDGE
            pw = Figure(title='WSIGMA',
                    x_axis_label='RA',
                    y_axis_label='DEC',
                    plot_height=350,
                    x_range=xrange_wedge,
                    y_range=yrange_wedge,
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




        # ================================
        # Stat histogram

        # x_fiber_hist
        d_yplt = (max(xsigma) - min(xsigma))*0.1
        yrange = [0, max(xsigma) + d_yplt]

        xhist = Plot2d(
            yrange,
            x_label="Fiber number",
            y_label="X std dev (number of pixels)",
            tooltip=xsigma_tooltip,
            title="",
            width=600,
            height=300,
            yscale="auto"
        ).quad(
            source,
            top='xsigma',
        )

        # w_fiber_hist
        d_yplt = (max(wsigma) - min(wsigma))*0.1
        yrange = [0, max(wsigma) + d_yplt]

        whist = Plot2d(
            yrange,
            x_label="Fiber number",
            y_label="W std dev (number of pixels)",
            tooltip=xsigma_tooltip,
            title="",
            width=600,
            height=300,
            yscale="auto"
        ).quad(
            source,
            top='wsigma',
        )

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
                yrange = (0.0*max(hist), 1.1*max(hist))
                bottomval = 'bottom'
                histval = 'hist'
            return [ylabel, yrange, bottomval, histval]


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

        yrangex = yrange


        p_hist_x = Figure(sizing_mode='scale_width',
                            title='', 
                            tools=[hover, "box_zoom,wheel_zoom,pan,reset"], 
                            active_drag="box_zoom", 
                            plot_height=300,
                            y_axis_label=ylabel, 
                            x_axis_label=xhistlabel,
                            background_fill_color="white", 
                            x_axis_type="auto", 
                            y_axis_type=yscale, 
                            y_range=yrange, 
                            x_range=(hist_rg[0]+xw_ref[0],
                                hist_rg[1]+xw_ref[0]), )

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

        p_hist_w = Figure(sizing_mode='scale_width', 
                            title='', 
                            tools=[hover, "box_zoom, pan,wheel_zoom,reset"], 
                            active_drag="box_zoom",
                            y_axis_label=ylabel, 
                            x_axis_label=xhistlabel, 
                            background_fill_color="white", 
                            plot_height=300, 
                            x_axis_type="auto",    
                            y_axis_type=yscale, 
                            y_range=yrange, 
                            x_range=(hist_rg[0]+xw_ref[1], 
                                    hist_rg[1] +xw_ref[1]), )

        p_hist_w.quad(top=histval, bottom=bottomval, left='left', right='right',
                      source=source_hist,
                      fill_color="dodgerblue", line_color='blue', alpha=0.8,
                      hover_fill_color='blue', hover_line_color='black', hover_alpha=0.8)

        # --------------------------------------------------------------
        # vlines ranges:
        bname = 'XWSIGMA'

        for ialert in nrg:  # par[bname+'_NORMAL_RANGE']:
            spans = Span(location=ialert+xw_ref[0], 
                        dimension='height',
                        line_color='green',
                        line_dash='dashed', line_width=2)
            p_hist_x.add_layout(spans)
            my_label = Label(x=ialert+xw_ref[0], 
                            y= yrangex[-1]/2.2,
                            y_units='data',
                            text='Normal Range',
                            text_color='green', angle=np.pi/2.)
            p_hist_x.add_layout(my_label)

        for ialert in wrg:  # par[bname+'_WARN_RANGE']:
            spans = Span(location=ialert+xw_ref[0], dimension='height', line_color='tomato',
                         line_dash='dotdash', line_width=2)
            p_hist_x.add_layout(spans)
            my_label = Label(x=ialert+xw_ref[0], y=yrangex[-1]/2.2, y_units='data',
                             text='Warning Range', text_color='tomato', angle=np.pi/2.)
            p_hist_x.add_layout(my_label)

        for ialert in nrg:  # par[bname+'_NORMAL_RANGE']:
            spans = Span(location=ialert+xw_ref[1], dimension='height', line_color='green',
                         line_dash='dashed', line_width=2)
            p_hist_w.add_layout(spans)
            my_label = Label(x=ialert+xw_ref[1], y=yrangew[-1]/2.2, y_units='data',
                             text='Normal Range', text_color='green', angle=np.pi/2.)
            p_hist_w.add_layout(my_label)

        for ialert in wrg:  # par[bname+'_WARN_RANGE']:
            spans = Span(location=ialert+xw_ref[1], dimension='height', line_color='tomato',
                         line_dash='dotdash', line_width=2)
            p_hist_w.add_layout(spans)
            my_label = Label(x=ialert+xw_ref[1], y=yrangew[-1]/2.2, y_units='data',
                             text='Warning Range', text_color='tomato', angle=np.pi/2.)
            p_hist_w.add_layout(my_label)


        # amp 1
        xamp = Patch().plot_amp(
            dz=xw_amp[0],
            refexp=[xw_ref[0]]*4,
            name="XSIGMA AMP",
            description="X standard deviation per Amp (number of pixels)",
            wrg=wrg
        )

        # amp 2
        wamp = Patch().plot_amp(
            dz=xw_amp[1],
            refexp=[xw_ref[1]]*4,
            name="WSIGMA AMP",
            description="W standard deviation per Amp (number of pixels)",
            wrg=wrg
        )

        # -------------------------------------------------------------------------
        info_col = Title().write_description('xwsigma')

        info = Table().mtable('xwsigma', mergedqa)

        alert_x = Table().alert_table(nrg, wrg)
        alert_w = Table().alert_table(nrg, wrg)

        if flavor == 'science':
            pxh = column(px, xhist, p_hist_x, xamp)
            pwh = column(pw, whist, p_hist_w, wamp)

            layout = column(
                info_col,
                widgetbox(Div(), css_classes=["tableranges"]),
                info,
                widgetbox(Div(), css_classes=["tableranges"]),
                widgetbox(Div(text='<h2 align=center style="text-align:center;">  XSIGMA </h2>')),
                widgetbox(Div(text='<h2 align=center style="text-align:center;">  WSIGMA </h2>')),
                alert_x,
                alert_w,
                column(px, sizing_mode='scale_both'),
                column(pw, sizing_mode='scale_both'),
                column(xhist, sizing_mode='scale_both'),
                column(whist, sizing_mode='scale_both'),
                column(p_hist_x, sizing_mode='scale_both'),
                column(p_hist_w, sizing_mode='scale_both'),
                column(xamp, sizing_mode='scale_both'),
                column(wamp, sizing_mode='scale_both'),
                css_classes=["display-grid"], sizing_mode='scale_width')
        else:
             layout = column(
                info_col,
                widgetbox(Div(), css_classes=["tableranges"]),
                widgetbox(tb_x),
                widgetbox(Div(), css_classes=["tableranges"]),
                widgetbox(Div(text='<h2 align=center style="text-align:center;">  XSIGMA </h2>')),
                widgetbox(Div(text='<h2 align=center style="text-align:center;">  WSIGMA </h2>')),
                widgetbox(tb_alert_x),
                widgetbox(tb_alert_w),
                # column(px, sizing_mode='scale_both'),
                # column(pw, sizing_mode='scale_both'),
                column(xhist, sizing_mode='scale_both'),
                column(whist, sizing_mode='scale_both'),
                column(p_hist_x, sizing_mode='scale_both'),
                column(p_hist_w, sizing_mode='scale_both'),
                column(xamp, sizing_mode='scale_both'),
                column(wamp, sizing_mode='scale_both'),
                css_classes=["display-grid"], sizing_mode='scale_width')
           
        return file_html(layout, CDN, "XWSIGMA")
