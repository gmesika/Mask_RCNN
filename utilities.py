import logging


def set_logger(context, verbose=False):

    logger = logging.getLogger(context)
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    #formatter = logging.Formatter(
    #    '%(levelname)-.1s:' + context + ':[%(filename).3s:%(funcName).3s:%(lineno)3d]:%(message)s', datefmt=
    #    '%m-%d %H:%M:%S')
    formatter = logging.Formatter(
        '%(levelname)-.1s:' + context + ':[%(filename).30s:%(funcName).30s:%(lineno)3d]:%(message)s', datefmt=
        '%m-%d %H:%M:%S')
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG if verbose else logging.INFO)
    console_handler.setFormatter(formatter)
    logger.handlers = []
    logger.addHandler(console_handler)
    return logger