from django.conf import settings


class ScrubRequestOnException(object):
    """
    Hide sensitive information so they're not recorded in error logging.
    * passwords in request.POST
    * sessionid in request.COOKIES
    """

    def process_exception(self, request, exception):
        # Get a copy so it's mutable.
        request.POST = request.POST.copy()
        for key in request.POST:
            if 'password' in key.lower():
                request.POST[key] = '******'

        # Remove session id from cookies
        if settings.SESSION_COOKIE_NAME in request.COOKIES:
            request.COOKIES[settings.SESSION_COOKIE_NAME] = '******'
            # Clearing out all cookies in request.META. They will already
            # be sent with request.COOKIES.
            request.META['HTTP_COOKIE'] = '******'
