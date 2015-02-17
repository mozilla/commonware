import threading

from django.utils import encoding


_local = threading.local()


def get_remote_addr():
    return getattr(_local, 'remote_addr', None)


def get_username():
    return getattr(_local, 'username', '<anon>')


class ThreadRequestMiddleware(object):
    """
    Store the current remote address in thread-local storage so our
    logging wrapper can access it.
    """

    def process_request(self, request):
        _local.remote_addr = request.META.get('REMOTE_ADDR', '')
        name = '<anon>'
        if hasattr(request, 'user') and request.user.is_authenticated():
            field = getattr(request.user, 'USERNAME_FIELD', 'username')
            name = encoding.smart_str(getattr(request.user, field, ''))
        _local.username = name
