from bokeh.layouts import widgetbox
from bokeh.models.widgets import Div

class Title:
    def write_description(self, qa_name):
        """Descriptions to be displayed in QA plots."""

        info_dic ={ 'countbins': ["Count Spectral Bins", 'Number of fibers with a nonzero number of bins above highest threshold'],
                        'skycont': ["Sky Continuum", 'Sky continuum in all configured continuum areas averaged over all sky fibers'],
                        'countpix': ["Count Pixels", 'Fraction of the pixels per amp that are above CUTPIX = 5 sigmas '],
                        'skypeak': ["Sky Peaks", 'Sky continuum in all configured continuum areas averaged over all sky fibers'],
                        'getbias': ["Bias From Overscan", 'Value of bias averaged over each amplifier'],
                        'getrms': ["Get RMS", 'Value of RMS for each amplifier read directly from the header of the pre processed image'],
                        'snr': ["Calculate SNR", 'List of average signal to noise ratio (SNR) for the N target type'],
                        'integ': ["Integrate Spectrum", 'List of the average fiber magnitude for each of N target types in this camera'],
                        'xwsigma': ["XWSigma", 'Fitted X and W SIGMA averaged over isolated bright sky wavelengths'],
                        'checkHDUs': ['',''],
                        'fiberflat':["Check Fiber Flat", "The average wavelength in the fiberflat frame"],
                        'arc':["Check ARC", """Number of fibers for which the first, second and third Legendre polynomial (P0, P1 and P2) in their""" \
                                +""" best-fit are outside 2 sigmas from the median of each"""],#"Number of fibers with Wsigma fit parameters (P0, P1, and P2) outside of 2 times RMS around medians"],
                        'xyshifts': ["XYSHIFTS","List of two averaged values (in pixel unit) for the fiber traces in X, Y directions"],
                        'skyR': ["SKYRBAND","Average value of sky background in R-band"],
                }
        
        text="""<body><p  style="text-align:left; color:#262626; font-size:1.5vw;">
                <b>{}</b> <br>{}</body>""".format(info_dic[qa_name][0],info_dic[qa_name][1])

        return widgetbox(Div(text=text), css_classes=["header"])