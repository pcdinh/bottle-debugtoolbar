import os

import bottle
from jinja2 import Environment, PackageLoader
from bottle_debugtoolbar.toolbar import DebugToolbar
from bottle_debugtoolbar.urls import url_quote_plus
from bottle_debugtoolbar.utils import replace_insensitive, _printable

# default config settings
default_config = {
    'DEBUG_TB_INTERCEPT_REDIRECTS': True,
    'DEBUG_TB_PANELS': (
        'bottle_debugtoolbar.panels.versions.VersionDebugPanel',
        'bottle_debugtoolbar.panels.timer.TimerDebugPanel',
        'bottle_debugtoolbar.panels.headers.HeaderDebugPanel',
        'bottle_debugtoolbar.panels.request_vars.RequestVarsDebugPanel',
        'bottle_debugtoolbar.panels.logger.LoggingPanel',
        'bottle_debugtoolbar.panels.profiler.ProfilerDebugPanel',
    )
}


class DebugToolbarPlugin(object):
    name = 'debugtoolbar'
    api  = 2

    _static_dir = os.path.realpath(
        os.path.join(os.path.dirname(__file__), 'static'))

    _redirect_codes = [301, 302, 303, 304]

    def __init__(self, config={}):
        self.app = None
        self.config = default_config
        self.config.update(config)
        self.debug_toolbar = None
        self.hosts = ()

    def setup(self, app):
        self.app = app

        if not self.enabled:
            return

        DebugToolbar.load_panels(self.config)

        self.hosts = self.config.get('DEBUG_TB_HOSTS', ())

        # Configure jinja for the internal templates and add url rules
        # for static data
        self.jinja_env = Environment(
            autoescape=True,
            extensions=['jinja2.ext.i18n', 'jinja2.ext.with_'],
            loader=PackageLoader(__name__, 'templates'))
        self.jinja_env.filters['urlencode'] = url_quote_plus
        self.jinja_env.filters['printable'] = _printable

        self.app.route(path='/_debug_toolbar/static/<filename:path>',
                       name='_debug_toolbar.static', 
                       callback=self.send_static_file)

    def apply(self, callback, route):
        def wrapper(*args, **kwargs):
            if self._show_toolbar():
                new_callback = self.process_request(callback, kwargs)
                try:
                    content = new_callback(*args, **kwargs)
                except bottle.HTTPResponse as e:
                    content = ''
                    bottle.response._status_code = e._status_code
                    bottle.response._status_line = e._status_line
                    bottle.response._headers = e._headers
                return self.process_response(content)
            else:
                return callback(*args, **kwargs)
        return wrapper

    @property
    def enabled(self):
        return self.config.get('DEBUG_TB_ENABLED', bottle.DEBUG)

    def _show_toolbar(self):
        """Return a boolean to indicate if we need to show the toolbar."""
        if not self.enabled:
            return False

        if bottle.request.path.startswith('/_debug_toolbar/'):
            return False

        if self.hosts and bottle.request.remote_addr not in self.hosts:
            return False

        return True

    def send_static_file(self, filename):
        """Send a static file from the bottle-debugtoolbar static directory."""
        return bottle.static_file(filename, root=self._static_dir)

    def process_request(self, view_func, view_kwargs):
        if not self._show_toolbar():
            return
        
        self.debug_toolbar = DebugToolbar(bottle.request, self.jinja_env)

        for panel in self.debug_toolbar.panels:
            panel.process_request(bottle.request)

        for panel in self.debug_toolbar.panels:
            new_view = panel.process_view(bottle.request, view_func, view_kwargs)
            if new_view:
                view_func = new_view
        return view_func

    def process_response(self, content):
        # Intercept http redirect codes and display an html page with a
        # link to the target.
        if self.config['DEBUG_TB_INTERCEPT_REDIRECTS']:
            if bottle.response.status_code in self._redirect_codes:
                redirect_to = bottle.response.headers['Location']
                redirect_code = bottle.response.status_code
                if redirect_to:
                    content = self.render('redirect.html', {
                        'redirect_to': redirect_to,
                        'redirect_code': redirect_code
                    })
                    bottle.response.content_length = len(content)
                    bottle.response.headers['Location'] = None
                    bottle.response.status = 200

        # If the http response code is 200 then we process to add the
        # toolbar to the returned html response.
        if (bottle.response.status_code == 200
            and bottle.response.headers['content-type'].startswith('text/html')):
            for panel in self.debug_toolbar.panels:
                panel.process_response(bottle.request, content)

            response_html = content.decode(bottle.response.charset)
            toolbar_html = self.debug_toolbar.render_toolbar()

            content = replace_insensitive(
                response_html, '</body>', toolbar_html + '</body>')
            content = content.encode(bottle.response.charset)
            bottle.response.content_length = len(content)
            return content

        return content

    def render(self, template_name, context):
        template = self.jinja_env.get_template(template_name)
        return template.render(**context)
