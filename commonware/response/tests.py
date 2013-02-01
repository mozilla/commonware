from django.conf import settings
from django.http import HttpResponse
from django.test.client import RequestFactory

import mock
from nose.tools import eq_

from commonware.response import decorators, middleware


view_fn = lambda *a: HttpResponse()


def _wrapped_resp(decorator, fn, mw_cls=None):
    req = RequestFactory().get('/')
    _wrapped = decorator(fn)
    resp = _wrapped(req)
    if mw_cls is not None:
        mw = mw_cls()
        resp = mw.process_response(req, resp)
    return resp


def _make_resp(mw_cls, secure=False):
    mw = mw_cls()
    req = RequestFactory().get('/')
    if secure:
        req.is_secure = lambda: True
    resp = mw.process_response(req, HttpResponse())
    return resp


def test_sts_middleware():
    resp = _make_resp(middleware.StrictTransportMiddleware)
    assert 'Strict-Transport-Security' not in resp
    resp = _make_resp(middleware.StrictTransportMiddleware, secure=True)
    assert 'Strict-Transport-Security' in resp
    eq_('max-age=31536000', resp['Strict-Transport-Security'])


@mock.patch.object(settings._wrapped, 'STS_SUBDOMAINS', True)
def test_sts_middleware_subdomains():
    resp = _make_resp(middleware.StrictTransportMiddleware, secure=True)
    assert 'Strict-Transport-Security' in resp
    assert resp['Strict-Transport-Security'].endswith('includeSubDomains')


def test_xframe_middleware():
    resp = _make_resp(middleware.FrameOptionsHeader)
    assert 'X-Frame-Options' in resp
    eq_('DENY', resp['X-Frame-Options'])


def test_xframe_middleware_no_overwrite():
    mw = middleware.FrameOptionsHeader()
    resp = HttpResponse()
    resp['X-Frame-Options'] = 'SAMEORIGIN'
    resp = mw.process_response({}, resp)
    eq_('SAMEORIGIN', resp['X-Frame-Options'])


def test_xframe_sameorigin_decorator():
    resp = _wrapped_resp(decorators.xframe_sameorigin, view_fn,
                         middleware.FrameOptionsHeader)
    assert 'X-Frame-Options' in resp
    eq_('SAMEORIGIN', resp['X-Frame-Options'])


def test_xframe_deny_middleware():
    resp = _wrapped_resp(decorators.xframe_deny, view_fn)
    assert 'X-Frame-Options' in resp
    eq_('DENY', resp['X-Frame-Options'])


def test_xframe_middleware_disable():
    resp = _wrapped_resp(decorators.xframe_allow, view_fn,
                         middleware.FrameOptionsHeader)
    assert not 'X-Frame-Options' in resp


def test_xssprotection_middleware():
    resp = _make_resp(middleware.XSSProtectionHeader)
    assert 'X-XSS-Protection' in resp
    eq_('1; mode=block', resp['X-XSS-Protection'])


def test_xssprotection_middleware_no_overwrite():
    mw = middleware.XSSProtectionHeader()
    resp = HttpResponse()
    resp['X-XSS-Protection'] = '1'
    resp = mw.process_response({}, resp)
    eq_('1', resp['X-XSS-Protection'])


def test_contenttypeoptions_middleware():
    resp = _make_resp(middleware.ContentTypeOptionsHeader)
    assert 'X-Content-Type-Options' in resp
    eq_('nosniff', resp['X-Content-Type-Options'])


def test_contenttypeoptions_middleware_no_overwrite():
    mw = middleware.ContentTypeOptionsHeader()
    resp = HttpResponse()
    resp['X-Content-Type-Options'] = ''
    resp = mw.process_response({}, resp)
    eq_('', resp['X-Content-Type-Options'])


def test_xrobotstag_middleware():
    resp = _make_resp(middleware.RobotsTagHeader)
    assert 'X-Robots-Tag' in resp
    eq_('noodp', resp['X-Robots-Tag'])


def test_xrobotstag_middleware_no_overwrite():
    mw = middleware.RobotsTagHeader()
    resp = HttpResponse()
    resp['X-Robots-Tag'] = 'bananas'
    resp = mw.process_response({}, resp)
    eq_('bananas', resp['X-Robots-Tag'])


def test_xrobots_exempt():
    resp = _wrapped_resp(decorators.xrobots_exempt, view_fn,
                         middleware.RobotsTagHeader)
    assert 'X-Robots-Tag' not in resp


def test_xrobots_tag_decorator():
    value = 'noindex,nofollow'
    resp = _wrapped_resp(decorators.xrobots_tag(value), view_fn,
                         middleware.RobotsTagHeader)
    assert 'X-Robots-Tag' in resp
    eq_(value, resp['X-Robots-Tag'])
