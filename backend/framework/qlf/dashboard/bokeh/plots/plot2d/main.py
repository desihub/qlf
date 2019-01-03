from bokeh.models import HoverTool, ColumnDataSource
from bokeh.plotting import Figure

class Plot2d:
    def __init__(self, yrange, x_title, y_title, tooltip, title="", width=600, height=400, yscale="auto", font_size="1vw"):
        hover = HoverTool(tooltips=tooltip)
        
        if yrange == None:
            self.plot = Figure(tools=[hover, "pan,wheel_zoom,box_zoom,reset, crosshair, tap"], plot_width=width, active_drag="box_zoom",
                        plot_height=height, background_fill_color="white", x_axis_type="auto", y_axis_type=yscale)

        else:
            self.plot = Figure(tools=[hover, "pan,wheel_zoom,box_zoom,reset, crosshair, tap"], plot_width=width, active_drag="box_zoom",
                        plot_height=height, background_fill_color="white", x_axis_type="auto", y_axis_type=yscale, y_range=yrange)
        
        self.plot.xaxis.axis_label = x_title
        self.plot.yaxis.axis_label = y_title

        self.plot.xaxis.major_label_text_font_size = font_size
        self.plot.yaxis.major_label_text_font_size = font_size
        self.plot.xaxis.axis_label_text_font_size = font_size
        self.plot.yaxis.axis_label_text_font_size = font_size
        self.plot.legend.label_text_font_size = font_size
        self.plot.title.text_font_size = font_size
        self.plot.title.text = title
        
    def vbar(self, source, y="y"):
        """
        2D Plots
        """
        self.plot.vbar(top=y, x='x', width=0.8,
                        source=source,
                        fill_color="dodgerblue", line_color="black", line_width=0.01, alpha=0.8,
                        hover_fill_color='red', hover_line_color='red', hover_alpha=0.8)

        return self.plot

    def quad(self, source, top, bottom='bottom', left='left', right='right', name='data'):
        self.plot.quad(top=top, bottom=bottom, left=left, right=right, name=name, source=source,
                   fill_color="dodgerblue", line_color="black", line_width=0.01, alpha=0.8,
                   hover_fill_color='red', hover_line_color='red', hover_alpha=0.8)
        return self.plot

    def line(self, source, x='x', y='y', color="black", line_width=1.5, line_alpha=0.9):
        self.plot.line(x=x, y=y, source=source,
                      color=color, line_width=line_width, line_alpha=line_alpha)
        return self

    def circle(self, source, x='x', y='y', color="blue", size=8, line_color='black', alpha=0.7, hover_color="blue", hover_alpha=1, hover_line_color='red'):
        self.plot.circle(x='x', y=y, source=source, 
                        color=color, size=size, line_color=line_color, alpha=alpha, 
                        hover_color=hover_color, hover_alpha=hover_alpha, hover_line_color=hover_line_color)
        return self