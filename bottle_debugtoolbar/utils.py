import os
import os.path
import sys

try:
    from pygments import highlight
    from pygments.formatters import HtmlFormatter
    from pygments.lexers import SqlLexer
    from pygments.styles import get_style_by_name
    PYGMENT_STYLE = get_style_by_name('colorful')
    HAVE_PYGMENTS = True
except ImportError:
    HAVE_PYGMENTS = False

cwd = os.getcwd()

def format_fname(value):
    # If the value is not an absolute path, the it is a builtin or
    # a relative file (thus a project file).
    if not os.path.isabs(value):
        if value.startswith(('{', '<')):
            return value
        if value.startswith('.' + os.path.sep):
            return value
        return '.' + os.path.sep + value

    # If the file is absolute and within the project root handle it as
    # a project file
    if value.startswith(cwd):
        return "." + value[len(cwd):]

    # Loop through sys.path to find the longest match and return
    # the relative path from there.
    paths = sys.path
    prefix = None
    prefix_len = 0
    for path in sys.path:
        new_prefix = os.path.commonprefix([path, value])
        if len(new_prefix) > prefix_len:
            prefix = new_prefix
            prefix_len = len(prefix)

    if not prefix.endswith(os.path.sep):
        prefix_len -= 1
    path = value[prefix_len:]
    return '<%s>' % path


def format_sql(query, args):
    if not HAVE_PYGMENTS:
        return query

    return highlight(
        query,
        SqlLexer(encoding='utf-8'),
        HtmlFormatter(encoding='utf-8', noclasses=True, style=PYGMENT_STYLE))


def replace_insensitive(string, target, replacement):
    """Similar to string.replace() but is case insensitive
    Code borrowed from: http://forums.devshed.com/python-programming-11/case-insensitive-string-replace-490921.html
    """
    no_case = string.lower()
    index = no_case.rfind(target.lower())
    if index >= 0:
        return string[:index] + replacement + string[index + len(target):]
    else: # no results so return the original string
        return string


def _printable(value):
    if isinstance(value, unicode):
        return value.encode('unicode_escape')
    elif isinstance(value, str):
        return value.encode('string_escape')
    else:
        return repr(value)
