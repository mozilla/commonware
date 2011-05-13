from django.conf import settings

import mock
from nose.tools import eq_
from test_utils import RequestFactory

from commonware.request.middleware import SetRemoteAddrFromForwardedFor


mw = SetRemoteAddrFromForwardedFor()


def get_req():
    req = RequestFactory().get('/')
    req.META['HTTP_X_FORWARDED_FOR'] = '1.2.3.4, 2.3.4.5'
    req.META['REMOTE_ADDR'] = '127.0.0.1'
    return req


def test_xff():
    req = get_req()
    mw.process_request(req)
    eq_('127.0.0.1', req.META['REMOTE_ADDR'])


@mock.patch.object(settings._wrapped, 'KNOWN_PROXIES', ['127.0.0.1'])
def test_xff_known():
    req = get_req()
    mw.process_request(req)
    eq_('2.3.4.5', req.META['REMOTE_ADDR'])

    req = get_req()
    del req.META['HTTP_X_FORWARDED_FOR']
    mw.process_request(req)
    eq_('127.0.0.1', req.META['REMOTE_ADDR'])


@mock.patch.object(settings._wrapped, 'KNOWN_PROXIES',
                   ['127.0.0.1', '2.3.4.5'])
def test_xff_multiknown():
    req = get_req()
    mw.process_request(req)
    eq_('1.2.3.4', req.META['REMOTE_ADDR'])


@mock.patch.object(settings._wrapped, 'KNOWN_PROXIES', ['127.0.0.1'])
def test_xff_bad_address():
    req = get_req()
    req.META['HTTP_X_FORWARDED_FOR'] += ',foobar'
    mw.process_request(req)
    eq_('2.3.4.5', req.META['REMOTE_ADDR'])


@mock.patch.object(settings._wrapped, 'KNOWN_PROXIES',
                   ['127.0.0.1', '2.3.4.5'])
def test_xff_all_known():
    """If all the remotes are known, use the last one."""
    req = get_req()
    req.META['HTTP_X_FORWARDED_FOR'] = '2.3.4.5'
    mw.process_request(req)
    eq_('2.3.4.5', req.META['REMOTE_ADDR'])
