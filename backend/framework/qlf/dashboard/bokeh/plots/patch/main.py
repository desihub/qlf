import numpy as np
from dashboard.bokeh.helper import get_palette
from bokeh.models import LinearColorMapper, ColorBar
from bokeh.models import HoverTool, PrintfTickFormatter, ColumnDataSource
from bokeh.plotting import Figure


class Patch:
    def set_amp(self, z_value):
        ''' Setup for AMP plots
        '''
        dz = z_value

        # removing NaN in ranges
        dz_valid = [x if x > -999 else np.nan for x in dz]
        dzmax, dzmin = np.nanmax(dz_valid), np.nanmin(dz_valid)

        if np.log10(dzmax) > 4 or np.log10(dzmin) < -3:
            ztext = ['{:4.2e}'.format(i) for i in dz_valid]
            cbarformat = "%2.1e"
        elif np.log10(dzmin) > 0:
            ztext = ['{:5.2f}'.format(i) for i in dz_valid]
            cbarformat = "%4.2f"
        else:
            ztext = ['{:6.2f}'.format(i) for i in dz_valid]
            cbarformat = "%5.2f"

        return ztext, cbarformat

    def val_status(self, val, nrg=[], wrg=[]):
        ''' Filtering results for status plot
        '''
        if val is None:
            return 'NaN'
        if val <=-999 or val == np.nan:
            return 'NaN'
        elif  val > nrg[0] and val < nrg[1]:
            return 'NORMAL'
        elif val < wrg[0] or val > wrg[1]:
            return 'ALARM'
        else:
            return 'WARNING'


    def plot_amp(self, dz, refexp, name="", font_size="1.2vw", description="", 
        nrg=[],wrg=[], status_plot=False):
        ''' Initializing AMP plot
        '''
        ztext, cbarformat = self.set_amp(dz)
        dx = [0, 1, 0, 1]
        dy = [1, 1, 0, 0]

        zvalid = np.array([x if x > -999 else np.nan for x in dz])
        data_source = dict(
                x=dx,
                y=dy,
                z=dz,
                zvalid=zvalid,
                ref=["{:.2f}".format(x) for x in refexp],
                zdiff=zvalid - np.array(refexp),
                y_offset1=[i+0.15 for i in dy],
                y_offset2=[i-0.10 for i in dy],
                amp=['AMP %s' % i for i in range(1, 5)],
                amp_number=['%s' % i for i in range(1, 5)],
                ztext=ztext,)

        if status_plot:
            text_val='status'
            color_status = ['green','darkgrey','yellow','red']
            color = {'NaN'    :'darkgrey',
                    'NORMAL'  :'green',
                    'WARNING' :'yellow',
                    'ALARM'   :'red',}
            status = [ self.val_status(x, nrg=nrg, wrg=wrg) for 
                                    x in zvalid - np.array(refexp) ]
            color_status = [ color[self.val_status(x, nrg=nrg, wrg=wrg)] for 
                                    x in zvalid - np.array(refexp) ]
            fill_color="color_status"
            data_source.update({'status':status,
                                'color_status':color_status,})
            fill_alpha=0.8

        if not status_plot:
            text_val='ztext'
            cmap = get_palette("RdBu_r")
            mapper = LinearColorMapper( palette=cmap,
                                        low=wrg[0],
                                        high=wrg[1],
                                        nan_color="darkgrey")
            formatter = PrintfTickFormatter(format=cbarformat)
            color_bar = ColorBar( color_mapper=mapper,  major_label_text_align='left',
                                  major_label_text_font_size='10pt', label_standoff=2, location=(0, 0),
                                  formatter=formatter, 
                                  title="(Val-Ref)", title_standoff=15, title_text_baseline="alphabetic")
            fill_color={'field': 'zdiff', 'transform': mapper}
            fill_alpha=0.9


        cmap_tooltip = """
            <div>

                <div>
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">AMP: </span>
                    <span style="font-size: 1vw; color: #515151;">@amp_number</span>
                </div>
                <div>
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">counts: </span>
                    <span style="font-size: 1vw; color: #515151">@text_val</span>
                </div>
                <div>
                    <span style="font-size: 1vw; font-weight: bold; color: #303030;">Reference: </span>
                    <span style="font-size: 1vw; color: #515151;">@ref</span>
                </div>
            </div>
        """.replace("counts:", name.replace("_AMP", "")+":").replace("text_val", text_val)

        hover = HoverTool(tooltips=cmap_tooltip)

        p = Figure(title=name, tools=[hover],
                   x_range=list([-0.5, 1.5]),
                   y_range=list([-0.5, 1.5]),
                   plot_width=450,
                   plot_height=400)

 
        source = ColumnDataSource(data= data_source)

        text_props = {
            "source": source,
            "angle": 0,
            "color": "black",
            "text_color": "black",
            "text_align": "center",
            "text_baseline": "middle"}

        p.rect("x", "y", .98, .98, 0, source=source,
               fill_color=fill_color, fill_alpha=fill_alpha)
        p.text(x="x", y="y_offset1", text="amp",
               text_font_size="2vw", **text_props)
        p.text(x="x", y="y_offset2", text="ztext",
               text_font_style="bold", text_font_size="2.5vw", **text_props)

        if not status_plot:
            p.add_layout(color_bar, 'right')

        # Format:
        p.xaxis.axis_label_text_font_size = font_size
        p.legend.label_text_font_size = font_size
        p.title.text_font_size = font_size
        p.xaxis.axis_label= description

        # Clear Axis:
        p.grid.grid_line_color = None
        p.outline_line_color = None
        p.axis.minor_tick_line_color = None
        p.axis.major_label_text_font_size = '0pt'
        p.yaxis.major_label_text_font_size = '0pt'
        p.xaxis.major_tick_line_color = None
        p.xaxis.minor_tick_line_color = None
        p.yaxis.major_tick_line_color = None
        p.yaxis.minor_tick_line_color = None
        p.yaxis.visible = False
        p.xaxis.visible = True
        p.axis.clear

        return p