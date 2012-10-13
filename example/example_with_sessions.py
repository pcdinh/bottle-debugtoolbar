#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import bottle
from beaker.middleware import SessionMiddleware
from bottle_debugtoolbar import DebugToolbarPlugin

config = {
    'DEBUG_TB_ENABLED': True,
    'DEBUG_TB_INTERCEPT_REDIRECTS': True,
}
plugin = DebugToolbarPlugin(config)
bottle.install(plugin)

session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 300,
    'session.data_dir': './data',
    'session.auto': True
}

@bottle.route('/')
def index():
    s = bottle.request.environ.get('beaker.session')
    s['test'] = s.get('test', 0) + 1
    s.save()
    return bottle.template('index')


@bottle.route('/redirect')
def redirect_example():
    bottle.response.set_cookie('test_cookie', '100')
    return bottle.redirect("/")


if __name__ == '__main__':
    bottle.debug(True)
    app = SessionMiddleware(bottle.app(), session_opts)
    bottle.run(app=app, host='localhost', port=8000, reloader=True)
