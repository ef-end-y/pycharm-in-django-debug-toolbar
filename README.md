## Pycharm Panel for Django Debug Toolbar ##
Adds a request history to [Django Debug Toolbar](https://github.com/django-debug-toolbar/django-debug-toolbar). For each request the plugin can run IDE to open the handler code file and put the cursor on the handler code first line. The plugin can also do this with ajax requests.

## Setup
```python
DEBUG_TOOLBAR_PANELS = [
    '...',
    '...',
    '...',
    'djdt_code_panel.CodeEditorPanel',
]
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