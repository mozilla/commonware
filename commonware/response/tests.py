from django.conf import settings
from django.http import HttpResponse
from django.test.client import RequestFactory

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


@mock.patch.object(middleware.statsd, 'incr')
def test_graphite_response(incr):
    req = RequestFactory().get('/')
    res = HttpResponse()
    gmw = middleware.GraphiteMiddleware()
    gmw.process_response(req, res)
    assert incr.called


@mock.patch.object(middleware.statsd, 'incr')
def test_graphite_response_authenticated(incr):
    req = RequestFactory().get('/')
    req.user = mock.Mock()
    req.user.is_authenticated.return_value = True
    res = HttpResponse()
    gmw = middleware.GraphiteMiddleware()
    gmw.process_response(req, res)
    eq_(incr.call_count, 2)


@mock.patch.object(middleware.statsd, 'incr')
def test_graphite_exception(incr):
    req = RequestFactory().get('/')
    ex = None
    gmw = middleware.GraphiteMiddleware()
    gmw.process_exception(req, ex)
    assert incr.called


@mock.patch.object(middleware.statsd, 'incr')
def test_graphite_exception_authenticated(incr):
    req = RequestFactory().get('/')
    req.user = mock.Mock()
    req.user.is_authenticated.return_value = True
    ex = None
    gmw = middleware.GraphiteMiddleware()
    gmw.process_exception(req, ex)
    eq_(incr.call_count, 2)


@mock.patch.object(middleware.statsd, 'timing')
def test_request_timing(timing):
    func = lambda x: x
    req = RequestFactory().get('/')
    res = HttpResponse()
    gmw = middleware.GraphiteRequestTimingMiddleware()
    gmw.process_view(req, func, tuple(), dict())
    gmw.process_response(req, res)
    eq_(timing.call_count, 3)
    names = ['view.%s.%s.GET' % (func.__module__, func.__name__),
             'view.%s.GET' % func.__module__,
             'view.GET']
    for expected, (args, kwargs) in zip(names, timing.call_args_list):
        eq_(expected, args[0])


@mock.patch.object(middleware.statsd, 'timing')
def test_request_timing_exception(timing):
    func = lambda x: x
    req = RequestFactory().get('/')
    res = HttpResponse()
    gmw = middleware.GraphiteRequestTimingMiddleware()
    gmw.process_view(req, func, tuple(), dict())
    gmw.process_exception(req, res)
    eq_(timing.call_count, 3)
    names = ['view.%s.%s.GET' % (func.__module__, func.__name__),
             'view.%s.GET' % func.__module__,
             'view.GET']
    for expected, (args, kwargs) in zip(names, timing.call_args_list):
        eq_(expected, args[0])
