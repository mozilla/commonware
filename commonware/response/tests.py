from django.http import HttpResponse

from nose.tools import eq_

from commonware.response import middleware


def test_force_tls_middleware():
    mw = middleware.StrictTransportMiddleware()
    resp = mw.process_response({}, HttpResponse())
    assert 'strict-transport-security' in resp
    eq_('max-age=2592000', resp['strict-transport-security'])


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
