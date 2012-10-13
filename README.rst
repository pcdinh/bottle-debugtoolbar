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


Screenshot
-----------

.. figure:: https://github.com/sramana/bottle-debugtoolbar/raw/master/docs/images/Bottle_Debug_Toolbar_Screenshot.png
   :width: 80%
   :align: center

Configuration
-------------

The toolbar support several configuration options:

====================================  =====================================   ==========================
Name                                  Description                             Default
====================================  =====================================   ==========================
``DEBUG_TB_ENABLED``                  Enable the toolbar?                     ``bottle.DEBUG``
``DEBUG_TB_HOSTS``                    Whitelist of hosts to display toolbar   any host
``DEBUG_TB_INTERCEPT_REDIRECTS``      Should intercept redirects?             ``True``
``DEBUG_TB_PANELS``                   List of module/class names of panels    enable all built-in panels
====================================  =====================================   ==========================


Contributing
------------

Fork us `on GitHub <https://github.com/sramana/bottle-debugtoolbar>`_
