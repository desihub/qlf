import logging
import os, sys

pattern = logging.Formatter("%(asctime)s %(message)s",
                            "%Y-%m-%d %H:%M:%S")


def get_logger(name, log_file=None, level=logging.INFO, formatter=pattern):
    """ Function to create logging.Logger class

    Arguments:
        name {str} -- log name

    Keyword Arguments:
        log_file {str} -- log file path
        level {int} -- log level (default: {logging.INFO == 20})
        formatter {logging.Formatter} -- log fommatter (default: {
            logging.Formatter(
                "%(asctime)s - %(message)s", "%Y-%m-%d %H:%M:%S"
            )
        })

    Returns:
        [logging.Logger] -- logging.Logger class
    """

    handler = logging.StreamHandler(sys.stdout)

    if log_file and os.environ.get('LOGS_DIRECTORY') != 'False':
        handler = logging.FileHandler(log_file)

    handler.setFormatter(formatter)

    log = logging.getLogger(name)
    log.setLevel(level)
    log.addHandler(handler)

    return log

if __name__ == "__main__":
    logger = get_logger("main_logger", "test_logger.log")
    logger.info('This is just info message')
