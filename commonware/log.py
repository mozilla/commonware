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


class Logger(logging.getLoggerClass()):
    """
    A wrapper for logging.Logger that adds the IP address to every logged
    message.

    To use CommonLogger instead of logging.Logger, you need to call
    logging.setLoggerClass(commonware.log.Logger)
    _before_ you set up your environment logging.
    """

    def __init__(self, name):
        logging.Logger.__init__(self, name)
    
    def _get_extra(self):
        return {'REMOTE_ADDR': get_remote_addr(),}

    def info(self, msg, *args):
        logging.Logger.info(self, msg % args, extra=self._get_extra())

    def debug(self, msg, *args):
        logging.Logger.debug(self, msg % args, extra=self._get_extra())

    def warning(self, msg, *args):
        logging.Logger.warning(self, msg % args, extra=self._get_extra())

    def error(self, msg, *args):
        logging.Logger.error(self, msg % args, extra=self._get_extra())

    def exception(self, msg, *args):
        logging.Logger.exception(self, msg % args, extra=self._get_extra())

    def critical(self, msg, *args):
        logging.Logger.exception(self, msg % args, extra=self._get_extra())
