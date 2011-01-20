from django.conf import settings


class FrameOptionsHeader(object):
    """
    Set an X-Frame-Options header. Default to DENY. Set
    response['x-frame-options'] = 'SAMEORIGIN'
    to override.
    """

    def process_response(self, request, response):
        if hasattr(response, 'no_frame_options'):
            return response

        if not 'x-frame-options' in response:
            response['x-frame-options'] = 'DENY'

        return response


class HttpOnlyMiddleware(object):
    """Set HttpOnly on all non-exempt cookies.

    You can exempt a cookie in two ways, either by adding it to the
    settings.JS_COOKIES list or by using the @js_cookies decorator, for
    example:

    @js_cookies('js_readable_cookie', 'readable_cookie')
    def my_view(request):

    Borrowed from:
        http://code.google.com/p/pageforest/source/browse/appengine/utils/cookies.py

    Compatible with Python 2.6+ only. Look at the URL for pre-2.6 support.
    """

    def process_response(self, request, response):
        cookies = getattr(settings, 'JS_COOKIES', [])
        if hasattr(response, 'js_cookies'):
            cookies += response.js_cookies
        for name in response.cookies:
            if name not in cookies:
                response.cookies[name]['httponly'] = True
        return response
