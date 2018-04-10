import logging

formatter = logging.Formatter("%(asctime)s - %(message)s",
                              "%Y-%m-%d %H:%M:%S")

def setup_logger(name, log_file, level=logging.INFO, handler=False):
    """Function setup as many loggers as you want"""

    if not handler:
        handler = logging.FileHandler(log_file)

    handler.setFormatter(formatter)

    log = logging.getLogger(name)
    log.setLevel(level)
    log.addHandler(handler)

    return log


if __name__ == "__main__":
    logger = setup_logger("main_logger", "test_logger.log")
    logger.info('This is just info message')
