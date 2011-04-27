import logging

# ThreadRequestMiddleware isn't used here but is imported so
# commonware.log.ThreadRequestMiddleware works.
from commonware.log.middleware import (get_remote_addr, get_username,
                                       ThreadRequestMiddleware)


def getLogger(name=None):
    """
    Wrap logging.getLogger to return a LoggerAdapter.

    If you need to do anything besides make logging calls, use
    logging.getLogger.
    """
    logger = logging.getLogger(name)
    return CommonwareAdapter(logger)


class CommonwareAdapter(logging.LoggerAdapter):
    """Adds the REMOTE_ADDR and USERNAME to every logging message's kwargs."""

    def __init__(self, logger, extra=None):
        logging.LoggerAdapter.__init__(self, logger, extra or {})

    def process(self, msg, kwargs):
        kwargs['extra'] = {'REMOTE_ADDR': get_remote_addr(),
                           'USERNAME': get_username()}
        return msg, kwargs


class Formatter(logging.Formatter):
    """Formatter that makes sure REMOTE_ADDR and USERNAME are available."""

    def format(self, record):
        for name in 'REMOTE_ADDR', 'USERNAME':
            record.__dict__.setdefault(name, '')
        return logging.Formatter.format(self, record)
