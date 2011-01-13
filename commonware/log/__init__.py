import logging

from commonware.log.middleware import get_remote_addr, ThreadRequestMiddleware


def getLogger(name=None):
    """
    Wrap logging.getLogger to return a LoggerAdapter.

    If you need to do anything besides make logging calls, use
    logging.getLogger.
    """
    logger = logging.getLogger(name)
    return RemoteAddrAdapter(logger)


class RemoteAddrAdapter(logging.LoggerAdapter):
    """Adds the REMOTE_ADDR to every logging message's kwargs."""

    def __init__(self, logger, extra=None):
        logging.LoggerAdapter.__init__(self, logger, extra or {})

    def process(self, msg, kwargs):
        kwargs['extra'] = {'REMOTE_ADDR': get_remote_addr()}
        return msg, kwargs


class Formatter(logging.Formatter):
    """Formatter that makes sure REMOTE_ADDR is available."""

    def format(self, record):
        if ('%(REMOTE_ADDR)' in self._fmt
            and 'REMOTE_ADDR' not in record.__dict__):
            record.__dict__['REMOTE_ADDR'] = None
        return logging.Formatter.format(self, record)
