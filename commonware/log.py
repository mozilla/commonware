import logging

from django.utils.thread_support import currentThread


_requests = {}


def get_request():
    return _requests.get(currentThread())


def set_request(request):
    _requests[currentThread()] = request


class ThreadRequestMiddleware(object):
    """
    Store the current request in thread-local storage so our logging
    wrapper can access it.
    """

    def process_request(request):
        set_request(request)


def getLogger(name):
    """
    Our own getLogger to return our logging wrapper around
    logging.Logger.
    """
    return CommonLogger(name)


class CommonLogger(logging.Logger):
    """
    A wrapper for logging.Logger that adds the IP address to every logged
    message.
    """
    
    extra = {}

    def _get_extra(self):
        if not self.extra:
            request = get_request()
            self.extra = {
                'REMOTE_ADDR': request.META.get('REMOTE_ADDR'),
            }
        return self.extra

    def info(self, msg):
        logging.Logger.info(self, msg, extra=self._get_extra())

    def debug(self, msg):
        logging.Logger.debug(self, msg, extra=self._get_extra())

    def warn(self, msg):
        logging.Logger.warn(self, msg, extra=self._get_extra())

    def error(self, msg):
        logging.Logger.error(self, msg, extra=self._get_extra())

    def exception(self, msg):
        logging.Logger.exception(self, msg, extra=self._get_extra())

    def critical(self, msg):
        logging.Logger.exception(self, msg, extra=self._get_extra())
        
    
