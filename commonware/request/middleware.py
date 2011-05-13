import socket

from django.conf import settings


class SetRemoteAddrFromForwardedFor(object):
    """
    Replaces the Django 1.1 middleware to replace the remote IP with
    the value of the X-Forwarded-For header for use behind reverse proxy
    servers, like load balancers.
    """

    def process_request(self, request):
        ips = []

        def is_valid(ip):
            try:
                socket.inet_aton(ip)
                return True
            except socket.error:
                return False

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
            if not ip in known:
                request.META['REMOTE_ADDR'] = ip
                break
