from threading import local


_local = local()


def get_remote_addr():
    return getattr(_local, 'addr', None)


def set_remote_addr(addr):
    _local.addr = addr


class ThreadRequestMiddleware(object):
    """
    Store the current remote address in thread-local storage so our
    logging wrapper can access it.
    """

    def process_request(self, request):
        set_remote_addr(request.META.get('REMOTE_ADDR', ''))
