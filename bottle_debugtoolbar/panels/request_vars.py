from bottle_debugtoolbar.panels import DebugPanel

_ = lambda x: x

class RequestVarsDebugPanel(DebugPanel):
    """
    A panel to display request variables (POST/GET, session, cookies).
    """
    name = 'RequestVars'
    has_content = True

    def nav_title(self):
        return _('Request Vars')

    def title(self):
        return _('Request Vars')

    def url(self):
        return ''

    def process_request(self, request):
        self.request = request
        self.view_func = None
        self.view_args = []
        self.view_kwargs = {}

    def process_view(self, request, view_func, view_kwargs):
        self.view_func = view_func
        self.view_kwargs = view_kwargs

    def content(self):
        context = self.context.copy()
        context.update({
            'get': self.request.query.items(),
            'post': self.request.forms.items(),
            'cookies': self.request.cookies.items(),
            'view_func': '%s.%s' % (self.view_func.__module__, self.view_func.__name__) if self.view_func else '[unknown]',
            'view_args': self.view_args,
            'view_kwargs': self.view_kwargs or {},
            'session': self.request.environ.get('beaker.session').items() if self.request.environ.get('beaker.session') else None,
        })

        return self.render('panels/request_vars.html', context)

