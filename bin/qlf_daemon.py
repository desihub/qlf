from dos_monitor import DOSmonitor
from qlf_pipeline import QLFPipeline

class QLFApp():

    def run(self):

        dos_monitor = DOSmonitor()
        night = dos_monitor.get_last_night()
        exposures = dos_monitor.get_exposures_by_night(night)

        for exposure in exposures:
            ql = QLFPipeline(exposure)

            if ql.was_processed():
                print(
                    "Exposure %s has already "
                    "been processed, skipping..." % exposure.get("expid")
                )
                continue

            ql.start_process()

if __name__ == "__main__":

    app = QLFApp()
    app.run()
