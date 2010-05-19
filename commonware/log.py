import logging

from django.utils.thread_support import currentThread


_requests = {}


def get_remote_addr():
    return _requests.get(currentThread())


def set_remote_addr(addr):
    _requests[currentThread()] = addr


class ThreadRequestMiddleware(object):
    """
    Store the current remote address in thread-local storage so our
    logging wrapper can access it.
    """

    def process_request(self, request):
        set_remote_addr(request.META.get('REMOTE_ADDR', ''))


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
