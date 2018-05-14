import logging

pattern = logging.Formatter("%(asctime)s - %(message)s",
                            "%Y-%m-%d %H:%M:%S")


def get_logger(name, log_file, level=logging.INFO, formatter=pattern, handler=False):
    """ Function to create log handlers """

    if not handler:
        handler = logging.FileHandler(log_file)

    handler.setFormatter(formatter)

    log = logging.getLogger(name)
    log.setLevel(level)
    log.addHandler(handler)

    return log


if __name__ == "__main__":
    logger = get_logger("main_logger", "test_logger.log")
    logger.info('This is just info message')
