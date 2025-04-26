"""
Copyright (c) 2023, Volyk Stanislav (https://github.com/ef-end-y/)
"""
import os
import inspect
import threading

from django.conf import settings
from django.http import HttpResponse
from django.urls import path, resolve, reverse
from django.utils.crypto import get_random_string
from django.utils.safestring import mark_safe

from debug_toolbar.panels import Panel
from debug_toolbar.toolbar import DebugToolbar
from django.utils.timezone import now


def open_editor(request, url_id):
    for _, toolbar in DebugToolbar._store.items():
        if data := toolbar.stats.get('CodeEditorPanel'):
            data = data['data']
            if url_id == data['id']:
                line, file = data['line'], data['file']
                cmd = settings.DJDT_CODE_EDITOR_PATH.format(line=line, file=file)
                os.system(cmd)
                return HttpResponse('<script>window.close()</script>')
    return HttpResponse('Not found')


class CodeEditorPanel(Panel):
    title = 'CodeEditor'
    nav_subtitle = ''
    is_async = True

    @staticmethod
    def _is_ajax(request):
        return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

    @classmethod
    def get_urls(cls):
        return [
            path('editor/open/<str:url_id>/', open_editor, name='open_editor'),
        ]

    @property
    def content(self):
        if self.has_content:
            stats = self.toolbar.stats.get(self.panel_id, {})
            message = stats.get('last_req_info', '') + '<br><br>'
            for _, toolbar in reversed(DebugToolbar._store.items()):
                if data := toolbar.stats.get('CodeEditorPanel'):
                    data = data['data']
                    message += data['date'].strftime('%H:%M:%S')
                    message += ' AJAX' if data['is_ajax'] else ''
                    message += ' ' + data['method']
                    href = reverse('djdt:open_editor', args=[data['id']])
                    message += f' <a href={href} target="_blank">{data["name"]}</a><br>'
            return mark_safe(message)

    def generate_stats(self, request, response):
        match = resolve(request.path)
        last_req_info = [f'Url name: <b>{match.url_name}</b>']

        func_path = match.func
        if hasattr(match.func, 'view_class'):
            view_class = match.func.view_class
            line_no = inspect.findsource(view_class)[1] + 1
            file = inspect.getfile(view_class)
            last_req_info.append(f'Class-based view: <b>{view_class.__name__}</b>')
        else:
            for i in range(10):  # max n decorator nesting
                if not hasattr(func_path, '__wrapped__'):
                    break
                func_path = func_path.__wrapped__
            func_name = match.func.__name__
            code = func_path.__code__
            line_no = getattr(code, 'co_firstlineno', 1)
            file = getattr(code, 'co_filename', None)
            if not isinstance(file, str) or not file.startswith('/'):
                file = inspect.getabsfile(func_path)
            last_req_info.append(f'Func name: <b>{func_name}</b>')
        
        last_req_info.append(f'File: <b>{file}</b>')

        self.record_stats({
            'last_req_info': '<br>'.join(last_req_info),
            'data': {
                'id': get_random_string(length=12),
                'date': now(),
                'is_ajax': self._is_ajax(request),
                'method': request.method,
                'name': match.url_name,
                'file': file,
                'line': line_no,
            }
        })
