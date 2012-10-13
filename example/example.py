#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import bottle
from bottle_debugtoolbar import DebugToolbarPlugin

config = {
    'DEBUG_TB_ENABLED': True,
    'DEBUG_TB_INTERCEPT_REDIRECTS': True,
}
plugin = DebugToolbarPlugin(config)
bottle.install(plugin)


@bottle.route('/')
def index():
    logging.warn("Hello")
    return bottle.template('index')


@bottle.route('/redirect')
def redirect_example():
    bottle.response.set_cookie('test_cookie', '100')
    return bottle.redirect("/")


if __name__ == '__main__':
    bottle.debug(True)
    bottle.run(host='localhost', port=8000, reloader=True)
