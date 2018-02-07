import logging
import psutil
import signal
import os

logger = logging.getLogger(name)


def reap_children(timeout=3):
    """Tries hard to terminate and ultimately kill all the children of this process.
    https://psutil.readthedocs.io/en/latest/#terminate-my-children """

    def on_terminate(proc):
        logger.info("process {} terminated with exit code {}".format(proc, proc.returncode))

    procs = psutil.Process().children()
    # send SIGTERM
    for p in procs:
        p.terminate()

    gone, alive = psutil.wait_procs(procs, timeout=timeout, callback=on_terminate)

    if alive:
        # send SIGKILL
        for p in alive:
            logger.info("process {} survived SIGTERM; trying SIGKILL" % p)
            p.kill()

        gone, alive = psutil.wait_procs(alive, timeout=timeout, callback=on_terminate)

        if alive:
            # give up
            for p in alive:
                logger.info("process {} survived SIGKILL; giving up" % p)


def kill_proc_tree(pid, sig=signal.SIGTERM, include_parent=True,
                   timeout=None, on_terminate=None):
    """Kill a process tree (including grandchildren) with signal
    "sig" and return a (gone, still_alive) tuple.
    "on_terminate", if specified, is a callabck function which is
    called as soon as a child terminates.
    """
    if pid == os.getpid():
        raise RuntimeError("I refuse to kill myself")

    parent = psutil.Process(pid)
    children = parent.children(recursive=True)

    if include_parent:
        children.append(parent)

    for p in children:
        p.send_signal(sig)

    gone, alive = psutil.wait_procs(children, timeout=timeout,
                                    callback=on_terminate)
    return (gone, alive)
