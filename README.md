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
