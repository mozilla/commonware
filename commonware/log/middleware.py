import threading


_local = threading.local()


def get_remote_addr():
    return getattr(_local, 'remote_addr', None)


def get_username():
    return getattr(_local, 'username', u'<anon>')


class ThreadRequestMiddleware(object):
    """
    Store the current remote address in thread-local storage so our
    logging wrapper can access it.
    """

    def process_request(self, request):
        _local.remote_addr = request.META.get('REMOTE_ADDR', u'')
        name = u'<anon>'
        if hasattr(request, 'user') and request.user.is_authenticated():
            name = request.user.username
        _local.username = name
