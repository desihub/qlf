import Pyro4
import os
from QLFInterface import ICSInterface

ics = ICSInterface.ICSInterface()


@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class ICSControl(object):
    def alarm(self, message):
        ics.alarm(message, level="EVENT")


def main():
    ics_daemon = os.environ.get('ICS_NAMESPACE', 'ICSDaemon')
    host = os.environ.get('ICS_HOST', 'localhost')
    port = int(os.environ.get('ICS_PORT', 50006))

    Pyro4.Daemon.serveSimple(
        {
            ICSControl: ics_daemon,
        },
        host=host,
        port=port,
        ns=False
    )


if __name__ == "__main__":
    main()
