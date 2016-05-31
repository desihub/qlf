from math import pi
from bokeh.plotting import Figure
from bokeh.models import Legend
from bokeh.models import DatetimeTickFormatter


def init_time_series_plot(hover):
    """
    Defaults for time series plot
    """
    plot = Figure(
        plot_height=300,
        plot_width=900,
        responsive=True,
        tools="xpan,xwheel_zoom,xbox_zoom,reset,tap",
        x_axis_type='datetime',
        min_border_top=0,
        min_border_right=10,
        min_border_bottom=50,
        min_border_left=50,
        outline_line_color=None,
    )
    plot.add_tools(hover)
    plot.x_range.follow = "end"
    plot.x_range.range_padding = 0
    plot.xaxis.axis_label = "Time"
    plot.xaxis.major_label_orientation = pi/4
    plot.xaxis.formatter = DatetimeTickFormatter(formats=dict(
        hours=["%d %B"],
        days=["%d %B"],
        months=["%d %B"],
        years=["%d %B"],
    ))
    return plot


def init_legend(legends):
    return Legend(
        legends=legends,
        location='top_right',
        border_line_color=None,
        background_fill_alpha=0.7
    )
