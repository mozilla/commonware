from django.conf import settings
from django.http import HttpResponse
from django.test.client import RequestFactory

import mock
from nose.tools import eq_

from commonware.response import middleware


def _make_resp(mw_cls, secure=False):
    mw = mw_cls()
    req = RequestFactory().get('/')
    if secure:
        req.is_secure = lambda: True
    resp = mw.process_response(req, HttpResponse())
    return resp


def test_sts_middleware():
    resp = _make_resp(middleware.StrictTransportMiddleware)
    assert 'strict-transport-security' not in resp
    resp = _make_resp(middleware.StrictTransportMiddleware, secure=True)
    assert 'strict-transport-security' in resp
    eq_('max-age=2592000', resp['strict-transport-security'])


@mock.patch.object(settings._wrapped, 'STS_SUBDOMAINS', True)
def test_sts_middleware_subdomains():
    resp = _make_resp(middleware.StrictTransportMiddleware, secure=True)
    assert 'strict-transport-security' in resp
    assert resp['strict-transport-security'].endswith('includeSubDomains')


def test_xframe_middleware():
    resp = _make_resp(middleware.FrameOptionsHeader)
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
