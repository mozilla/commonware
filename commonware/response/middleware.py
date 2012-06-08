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


class RobotsTagHeader(object):
    """Set an X-Robots-Tag header. Default to noodp."""

    def process_response(self, request, response):
        if not 'x-robots-tag' in response:
            response['x-robots-tag'] = 'noodp'

        return response


class StrictTransportMiddleware(object):
    """
    Set the Strict-Transport-Security header on responses. Use the
    STS_MAX_AGE setting to control the max-age value. (Default: 1 month.)
    Use the STS_SUBDOMAINS boolean to add includeSubdomains.
    (Default: False.)
    """

    def process_response(self, request, response):
        if request.is_secure():
            age = getattr(settings, 'STS_MAX_AGE', 2592000)  # 30 days.
            subdomains = getattr(settings, 'STS_SUBDOMAINS', False)
            val = 'max-age=%d' % age
            if subdomains:
                val += '; includeSubDomains'
            response['Strict-Transport-Security'] = val
        return response
