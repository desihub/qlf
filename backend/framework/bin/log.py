import logging
import os
import sys

pattern = logging.Formatter("%(asctime)s %(message)s",
                            "%Y-%m-%d %H:%M:%S")


def get_logger(name, log_file, level=logging.INFO, formatter=pattern):
    """ Function to create logging.Logger class

    Arguments:
        name {str} -- log name
        log_file {str} -- log file path

    Keyword Arguments:
        level {int} -- log level (default: {logging.INFO == 20})
        formatter {logging.Formatter} -- log fommatter (default: {
            logging.Formatter(
                "%(asctime)s - %(message)s", "%Y-%m-%d %H:%M:%S"
            )
        })

    Returns:
        [logging.Logger] -- logging.Logger class
    """
    if os.environ.get('LOGS_DIRECTORY') == 'False':
        log = logging.getLogger(__name__)
        out_hdlr = logging.StreamHandler(sys.stdout)
        out_hdlr.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
        out_hdlr.setLevel(logging.INFO)
        log.addHandler(out_hdlr)
        log.setLevel(logging.INFO)
        return log
    else:
        handler = logging.FileHandler(log_file)
        handler.setFormatter(formatter)

        log = logging.getLogger(name)
        log.setLevel(level)
        log.addHandler(handler)

        return log



if __name__ == "__main__":
    logger = get_logger("main_logger", "test_logger.log")
    logger.info('This is just info message')
