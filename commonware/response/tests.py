from django.conf import settings
from django.http import HttpResponse

import mock
from nose.tools import eq_

from commonware.response import middleware


def test_sts_middleware():
    mw = middleware.StrictTransportMiddleware()
    resp = mw.process_response({}, HttpResponse())
    assert 'strict-transport-security' in resp
    eq_('max-age=2592000', resp['strict-transport-security'])


@mock.patch.object(settings._wrapped, 'STS_SUBDOMAINS', True)
def test_sts_middleware_subdomains():
    mw = middleware.StrictTransportMiddleware()
    resp = mw.process_response({}, HttpResponse())
    assert 'strict-transport-security' in resp
    assert resp['strict-transport-security'].endswith('includeSubDomains')


def test_xframe_middleware():
    mw = middleware.FrameOptionsHeader()
    resp = mw.process_response({}, HttpResponse())
    assert 'x-frame-options' in resp
    eq_('DENY', resp['x-frame-options'])


def test_xframe_middleware_no_overwrite():
    mw = middleware.FrameOptionsHeader()
    resp = HttpResponse()
    resp['x-frame-options'] = 'SAMEORIGIN'
    resp = mw.process_response({}, resp)
    eq_('SAMEORIGIN', resp['x-frame-options'])


def test_xframe_middleware_disable():
    mw = middleware.FrameOptionsHeader()
    resp = HttpResponse()
    resp.no_frame_options = True
    resp = mw.process_response({}, resp)
    assert not 'x-frame-options' in resp
