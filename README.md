## Pycharm Panel for Django Debug Toolbar ##
Adds a request history to [Django Debug Toolbar](https://github.com/django-debug-toolbar/django-debug-toolbar). This plugin can run pycharm to open the handler code file and put the cursor on the handler code first line. The plugin can also do this with ajax requests.

## Setup
```python
DEBUG_TOOLBAR_PANELS = [
    '...',
    '...',
    '...',
    'pycharm_panel.PycharmUrlPanel'
]
```

DJDT_PYCHARM_PATH = '/path/to/pycharm-professional'

## Limitations

The plugin does not do code analysis. It just opens the target file and looks for a line like "def view_name(" or "class ViewClass(". But it works. In most cases :)
