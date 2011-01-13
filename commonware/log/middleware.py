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
