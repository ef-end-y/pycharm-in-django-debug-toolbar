"""
Copyright (c) 2023, Volyk Stanislav (https://github.com/ef-end-y/)
"""
import os
import inspect
import threading
from importlib import import_module

from django.conf import settings
from django.http import HttpResponse
from django.urls import path, resolve, reverse
from django.utils.crypto import get_random_string
from django.utils.safestring import mark_safe

from debug_toolbar.panels import Panel
from django.utils.timezone import now


T_LOCAL = threading.local()
T_LOCAL.djdt_url_log = []


def get_url_log() -> list:
    if not hasattr(T_LOCAL, 'djdt_url_log'):
        T_LOCAL.djdt_url_log = []
    return T_LOCAL.djdt_url_log


def open_pycharm(request, url_id):
    for data in get_url_log():
        if url_id == data['id']:
            search_line, file = data['search'], data['file']
            with open(file, 'r') as f:
                content = f.read()
                for line, value in enumerate(content.split('\n')):
                    if value.startswith(search_line):
                        os.system(f'{settings.DJDT_PYCHARM_PATH} --line {line} {file}')
                        return HttpResponse('<script>window.close()</script>')
            return HttpResponse(f'Not found code for url {data["name"]} :(')
    return HttpResponse('Not found')


class PycharmUrlPanel(Panel):
    title = 'Pycharm'
    nav_subtitle = ''

    @classmethod
    def get_urls(cls):
        return [
            path('pycharm/open/<str:url_id>/', open_pycharm, name='open_pycharm'),
        ]

    @property
    def content(self):
        if self.has_content:
            stats = self.toolbar.stats.get(self.panel_id, {})
            message = stats.get('last_url_info', '') + '<br><br>'
            for data in get_url_log():
                message += data['date'].strftime('%H:%M:%S')
                message += ' AJAX' if data['is_ajax'] else ''
                message += ' ' + data['method']
                href = reverse('djdt:open_pycharm', args=[data['id']])
                message += f' <a href={href} target="_blank">{data["name"]}</a><br>'
            return mark_safe(message)

    def generate_stats(self, request, response):
        match = resolve(request.path)
        last_url_info = [f'Url name: <b>{match.url_name}</b>']

        func_path = match.func
        if hasattr(match.func, 'view_class'):
            func_name = match.func.__name__
            last_url_info.append(f'This is class-based view: <b>{func_name}</b>')
            search_line = f'class {func_name}('
            file = import_module(match.func.__module__).__file__
        else:
            for i in range(10):  # max n decorator nesting
                if not hasattr(func_path, '__wrapped__'):
                    break
                func_path = func_path.__wrapped__
            func_name = match.func.__name__
            last_url_info.append(f'Func name: <b>{func_name}</b>')
            search_line = f'def {func_name}('
            file = os.path.abspath(inspect.getfile(func_path))
        last_url_info.append(f'File: <b>{file}</b>')

        url_log = get_url_log()
        url_log.insert(0, {
            'id': get_random_string(),
            'date': now(),
            'is_ajax': request.is_ajax(),
            'method': request.method,
            'name': match.url_name,
            'file': file,
            'search': search_line,
        })
        del url_log[30:]

        self.record_stats({'last_url_info': '<br>'.join(last_url_info)})
