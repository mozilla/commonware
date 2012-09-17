import socket

from django.conf import settings

TYPES = (socket.AF_INET, socket.AF_INET6)


def is_valid(ip):
    for af in TYPES:
        try:
            socket.inet_pton(af, ip)
            return True
        except socket.error:
            pass
    return False


class SetRemoteAddrFromForwardedFor(object):
    """
    Replaces the Django 1.1 middleware to replace the remote IP with
    the value of the X-Forwarded-For header for use behind reverse proxy
    servers, like load balancers.
    """

    def process_request(self, request):
        ips = []

        if 'HTTP_X_FORWARDED_FOR' in request.META:
            xff = [i.strip() for i in
                   request.META['HTTP_X_FORWARDED_FOR'].split(',')]
            ips = [ip for ip in xff if is_valid(ip)]
        else:
            return

        ips.append(request.META['REMOTE_ADDR'])

        known = getattr(settings, 'KNOWN_PROXIES', [])
        ips.reverse()
        for ip in ips:
            request.META['REMOTE_ADDR'] = ip
            if not ip in known:
                break
