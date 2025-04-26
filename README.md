## Pycharm Panel for Django Debug Toolbar ##
Open http://your.site/path/to/somewhere in your Django project. Do you want to see what part of the code handles that url? One click and an editor will be opened with cursor at the right place. This is a plugin for [Django Debug Toolbar](https://github.com/django-debug-toolbar/django-debug-toolbar).

## Setup
```python
DEBUG_TOOLBAR_PANELS = [
    # '...',
    # '...',
    # '...',
    'djdt_code_panel.CodeEditorPanel',
]
```

for example:
```python
DEBUG_TOOLBAR_PANELS = {
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    'djdt_code_panel.CodeEditorPanel',
}
```

path to your IDE:
```python
DJDT_CODE_EDITOR_PATH = '/path/to/your/ide'
```

for example:
```python
DJDT_CODE_EDITOR_PATH = 'pycharm-professional --line {line} {file}'
DJDT_CODE_EDITOR_PATH = '/Applications/PyCharm\ CE.app/Contents/MacOS/pycharm --line {line} {file}'
DJDT_CODE_EDITOR_PATH = '/usr/bin/code -r -g {file}:{line}'  # Visual Studio Code
```
