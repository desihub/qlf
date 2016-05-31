from bokeh.models import ColumnDataSource, OpenURL, TapTool
from bokeh.models import HoverTool
from .defaults import init_time_series_plot, init_legend
from ..models import get_time_series_data


def make_time_series_plot(metric):

    legends = []

    data = get_time_series_data(metric)

    source = ColumnDataSource(
            data=dict(x=data['dates'], y=data['values'],
                      desc=data['id']),
        )

    hover = HoverTool(tooltips=[("Job ID", "@desc"),
                                (data['metric'], "@y "+data['units'])])

    plot = init_time_series_plot(hover=hover)

    line = plot.line(
            x='x', y='y', source=source,
            line_width=2, line_cap='round'
        )

    plot.circle(x='x', y='y', source=source, fill_color="white", size=16)

    taptool = plot.select(type=TapTool)

    taptool.callback = OpenURL(url="www.example.com")

    plot.yaxis.axis_label = data['metric'] + '(' + data['units'] + ')'

    legends.append((data['metric'], [line]))

    plot.add_layout(init_legend(legends=legends))

    return plot
