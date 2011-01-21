from nose.tools import eq_
from test_utils import RequestFactory

from commonware.request.middleware import SetRemoteAddrFromForwardedFor


def test_remote_addr():
    tests = (
        ('1, 2, 3, 4', '1'),
        ('1.2.3.4', '1.2.3.4'),
        (None, '127.0.0.1'),
    )

    srafff = SetRemoteAddrFromForwardedFor()
    get = RequestFactory().get('/foo')

    def check_output(x, r):
        if x:
            get.META['HTTP_X_FORWARDED_FOR'] = x
        else:
            del get.META['HTTP_X_FORWARDED_FOR']

        get.META['REMOTE_ADDR'] = '127.0.0.1'
        srafff.process_request(get)
        eq_(get.META['REMOTE_ADDR'], r)

    for x, r in tests:
        yield check_output, x, r
