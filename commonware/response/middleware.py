from django.conf import settings


class FrameOptionsHeader(object):
    """
    Set an X-Frame-Options header. Default to DENY. Set
    response['X-Frame-Options'] = 'SAMEORIGIN'
    to override.
    """

    def process_response(self, request, response):
        if hasattr(response, 'no_frame_options'):
            return response

        if 'X-Frame-Options' not in response:
            response['X-Frame-Options'] = 'DENY'

        return response


class RobotsTagHeader(object):
    """Set an X-Robots-Tag header.

    Default to noodp to avoid using directories for page titles. Set
    a value of response['X-Robots-Tag'] or use the relevant decorators
    to override.

    Change the default in settings by setting X_ROBOTS_DEFAULT = ''.
    """

    def process_response(self, request, response):
        if getattr(response, 'no_robots_tag', False):
            return response

        if 'X-Robots-Tag' not in response:
            default = getattr(settings, 'X_ROBOTS_DEFAULT', 'noodp')
            response['X-Robots-Tag'] = default

        return response


class XSSProtectionHeader(object):
    """
    Set the X-XSS-Protection header on responses. Defaults to
    '1; mode=block'. Set response['X-XSS-Protection'] = '0' (disable)
    or '1' (rewrite mode) to override.
    """

    def process_response(self, request, response):
        if 'X-XSS-Protection' not in response:
            response['X-XSS-Protection'] = '1; mode=block'
        return response


class ContentTypeOptionsHeader(object):
    """
    Set the X-Content-Type-Options header on responses. Defaults
    to 'nosniff'. Set response['X-Content-Type-Options'] = ''
    to override.
    """

    def process_response(self, request, response):
        if 'X-Content-Type-Options' not in response:
            response['X-Content-Type-Options'] = 'nosniff'
        return response
