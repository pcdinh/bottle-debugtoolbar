Bottle Debug Toolbar
=====================

This is a port of the `flask-debug-toolbar <https://github.com/mgood/flask-debugtoolbar>`_ (which is a port of the `django-debug-toolbar <https://github.com/django-debug-toolbar/django-debug-toolbar>`_) for Bottle applications.


Installation
------------

Installing is simple with pip::

    $ pip install bottle-debugtoolbar


Usage
-----

Setting up the debug toolbar is simple::

    import bottle
    from bottle_debugtoolbar import DebugToolbarPlugin

    config = {
        'DEBUG_TB_ENABLED': True,
        'DEBUG_TB_INTERCEPT_REDIRECTS': True,
    }
    plugin = DebugToolbarPlugin(config)
    bottle.install(plugin)


See the `documentation`_ for more information.

.. _documentation: http://bottle-debugtoolbar.readthedocs.org
