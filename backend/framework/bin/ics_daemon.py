import Pyro4
from QLFInterface import ICSInterface
from clients import (ICS_DAEMON_NS, PYRO_HOST,
                     PYRO_PORT, get_ics_daemon)

ics = ICSInterface.ICSInterface()


@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class ICSControl(object):
    def alarm(self, message):
        ics.alarm(message, level="EVENT")

    def test(self):
        return 'testing'


def main():
    ics_daemon = ICS_DAEMON_NS
    host = PYRO_HOST
    port = int(PYRO_PORT)

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
