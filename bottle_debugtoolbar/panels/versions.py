from bottle import __version__ as bottle_version
from bottle_debugtoolbar.panels import DebugPanel

_ = lambda x: x

class VersionDebugPanel(DebugPanel):
    """
    Panel that displays the Bottle version.
    """
    name = 'Version'
    has_content = False

    def nav_title(self):
        return _('Versions')

    def nav_subtitle(self):
        return 'Bottle %s' % bottle_version

    def url(self):
        return ''

    def title(self):
        return _('Versions')

    def content(self):
        return None


