'''
Notification features:
- text scrolls
- available icon option
- markup turned by default on
- title will be shortened if too long
- object
- methods:
  - open
    -returns Thread

TODO:
- linux & osx window hide & grab focus back implementation
  (needed for hiding the window another python interpreter creates)
- position relatively to the taskbar (or at least not on top of it)
- forbid notification to print Kivy initialisation logs to output
  unless asked for it
'''

import sys
import threading
from subprocess import call as scall
from os.path import dirname, abspath, join
from kivy.app import App


class Notification(object):
    def open(self, title='Title', message='Message', icon=None,
             width=300, height=100, offset_x=10, offset_y=40,
             timeout=15, timeout_close=True,
             line_color=(.2, .64, .81, .5), color=(0, 0, 0, 1),
             background_color=(.92, .92, .92, 1),
             parent_title=None):

        if not parent_title:
            app = App.get_running_app()
            parent_title = app.get_application_name()

        self.path = dirname(abspath(__file__))
        t = threading.Thread(target=self._call, args=str({
            'title': title,
            'message': message,
            'icon': icon,
            'width': width,
            'height': height,
            'offset_x': offset_x,
            'offset_y': offset_y,
            'timeout': timeout,
            'timeout_close': timeout_close,
            'line_color': line_color,
            'color': color,
            'background_color': background_color,
            'parent_title': parent_title
        }))

        t.start()
        return t

    def _call(self, *args):
        scall([
            sys.executable,
            join(self.path, 'notification.py'),
            ''.join(args)  # need for 2.7.9, converts tuple
        ])
