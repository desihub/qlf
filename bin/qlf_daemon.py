from dos_monitor import DOSmonitor
from qlf_pipeline import QLFPipeline

class QLFApp():

    def run(self):

        dos_monitor = DOSmonitor()
        night = dos_monitor.get_last_night()
        exposures = dos_monitor.get_exposures_by_night(night)

        for exposure in exposures:
            ql = QLFPipeline(exposure)
            ql.start_process()

if __name__ == "__main__":

    app = QLFApp()
    app.run()
