from bokeh.models import HoverTool, ColumnDataSource, PrintfTickFormatter
from bokeh.plotting import Figure
from bokeh.models import ColorBar
from bokeh.models.glyphs import Segment
from bokeh.models import FixedTicker

class Plot2d:
    def __init__(self, x_range=None, y_range=None, x_label="", y_label="", tooltip=None, title="", width=600, height=400, yscale="auto", font_size="1vw", hover_mode="mouse"):
        hover = HoverTool(tooltips=tooltip, mode=hover_mode)

        if y_range == None:
            self.plot = Figure(
                tools=[hover,"pan,wheel_zoom,box_zoom,reset,crosshair,tap"],
                plot_width=width,
                active_drag="box_zoom",
                plot_height=height,
                background_fill_color="white",
                x_axis_type="auto",
                y_axis_type=yscale
            )
        else:
            self.plot = Figure(
                tools=[hover,"pan,wheel_zoom,box_zoom,reset,crosshair,tap"],
                plot_width=width,
                active_drag="box_zoom",
                plot_height=height,
                background_fill_color="white",
                x_axis_type="auto",
                y_axis_type=yscale,
                y_range=y_range,
                x_range=x_range
            )

        self.plot.xaxis.axis_label = x_label
        self.plot.yaxis.axis_label = y_label

        self.plot.xaxis.major_label_text_font_size = font_size
        self.plot.yaxis.major_label_text_font_size = font_size
        self.plot.xaxis.axis_label_text_font_size = font_size
        self.plot.yaxis.axis_label_text_font_size = font_size
        self.plot.legend.label_text_font_size = font_size
        self.plot.title.text_font_size = font_size
        self.plot.title.text = title

    def vbar(self, source, y="y", x="x", line_width=0.01):
        self.plot.vbar(
            top=y,
            x=x,
            width=0.8,
            source=source,
            fill_color="dodgerblue",
            line_color="black",
            line_width=line_width,
            alpha=0.8,
            hover_fill_color='red',
            hover_line_color='red',
            hover_alpha=0.8
        )
        return self.plot

    def quad(self, source, top, bottom='bottom', left='left', right='right', name='data', line_width=0.1):
        self.plot.quad(
            top=top,
            bottom=bottom,
            left=left,
            right=right,
            name=name,
            source=source,
            fill_color="dodgerblue",
            line_color="black",
            line_width=line_width,
            alpha=0.8,
            hover_fill_color='red',
            hover_line_color='red',
            hover_alpha=0.8
        )
        return self.plot

    def line(self, source, x='x', y='y', color="black", line_width=1.5, line_alpha=0.9):
        self.plot.line(
            x=x,
            y=y,
            source=source,
            color=color,
            line_width=line_width,
            line_alpha=line_alpha
        )
        return self


    def circle(
        self,
        source,
        x='x',
        y='y',
        color="blue",
        size=8,
        line_color='black',
        alpha=0.7,
        hover_color="blue",
        hover_alpha=1,
        hover_line_color='red',
        radius=0.0165,
        fill_color='lightgray',
        line_width=0.3,
        hover_fill_color=None
    ):
        self.plot.circle(
            x=x,
            y=y,
            source=source,
            color=color,
            size=size,
            line_color=line_color,
            alpha=alpha,
            hover_color=hover_color,
            hover_alpha=hover_alpha,
            hover_line_color=hover_line_color,
            fill_color=fill_color,
            hover_fill_color=hover_fill_color,
        )
        return self

    def set_colorbar(self,z_value):
        ''' Setup for colorbar
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

    def colorbar(self, mapper, title='(Val - Ref)'):
        formatter = PrintfTickFormatter(format="%4.2f")

        color_bar = ColorBar(color_mapper=mapper, label_standoff=16,
                                title=title,
                                major_label_text_font_style='bold', padding=26,
                                major_label_text_align='left',
                                major_label_text_font_size="10pt",
                                formatter=formatter,
                                title_text_baseline='alphabetic',
                                location=(0, 0))
        self.plot.add_layout(color_bar, 'right')
        return self

    def wedge(self, source, field=None, x="x", y="y", mapper=None, radius=0.0165, colorbar_title='counts'):

        if mapper:
            self.plot = self.circle(
                source,
                y=y,
                x=x,
                radius=radius,
                fill_color={'field': field, 'transform': mapper},
                line_color='black',
                line_width=0.3,
            ).circle(
                source,
                y=y,
                x=x,
                radius=radius+0.005,
                fill_color=None,
                line_color=None,
                line_width=3,
                hover_fill_color={'field': field, 'transform': mapper},
                hover_line_color='red'
            ).colorbar(mapper, title=colorbar_title).plot
        elif field:
            self.plot = self.circle(
                source,
                y=y,
                x=x,
                radius=radius,
                hover_fill_color='lightgrey',
                fill_color={'field': 'color'},
                line_color='black',
                line_width=0.3,
            ).plot
        else:
            self.plot = self.circle(
                source,
                y=y,
                x=x,
                radius=radius,
                hover_fill_color='lightgrey',
                fill_color='darkgrey',
                line_color='black',
                line_width=0.3,
            ).plot

        return self

    def segment(self, source, x0='segx0', x1='segx1', y0='segy0',
                y1='segy1', line_width=2, line_color='#1e90ff'):
        seg = Segment(x0=x0, x1=x1, y0=y0,
                      y1=y1, line_width=line_width, line_color=line_color)

        self.plot.add_glyph(source, seg)

        self.plot.yaxis.ticker = FixedTicker(ticks=[0, 1])
        self.plot.yaxis.major_label_overrides = {'0': 'bad', '1': 'good'}
        return self
