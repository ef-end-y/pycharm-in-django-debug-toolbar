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
from django.utils.timezone import now


T_LOCAL = threading.local()
T_LOCAL.djdt_request_log = []


def get_request_log() -> list:
    if not hasattr(T_LOCAL, 'djdt_request_log'):
        T_LOCAL.djdt_request_log = []
    return T_LOCAL.djdt_request_log


def open_editor(request, url_id):
    for data in get_request_log():
        if url_id == data['id']:
            line, file = data['line'], data['file']
            os.system(f'{settings.DJDT_PYCHARM_PATH} --line {line} {file}')
            return HttpResponse('<script>window.close()</script>')
    return HttpResponse('Not found')


class PycharmUrlPanel(Panel):
    title = 'Pycharm'
    nav_subtitle = ''

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
            for data in get_request_log():
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
            func_name = match.func.__name__
            class_ref = getattr(inspect.getmodule(match.func), func_name)
            line_no = inspect.findsource(class_ref)[1] + 1
            file = inspect.getfile(class_ref)
            last_req_info.append(f'Class-based view: <b>{func_name}</b>')
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

        request_log = get_request_log()
        request_log.insert(0, {
            'id': get_random_string(length=12),
            'date': now(),
            'is_ajax': self._is_ajax(request),
            'method': request.method,
            'name': match.url_name,
            'file': file,
            'line': line_no,
        })
        del request_log[30:]

        self.record_stats({'last_req_info': '<br>'.join(last_req_info)})
