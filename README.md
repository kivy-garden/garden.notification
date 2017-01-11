# garden.notification
:name_badge: A floating popup-like notification

<img src="https://raw.githubusercontent.com/kivy-garden/garden.notification/master/screenshot.png"></img>

Only Windows for now, due to missing api for screen resolution.
Hopefully will be fixed soon.

## Example:

```
from kivy.app import App
from kivy.lang import Builder
from kivy.resources import resource_find
from kivy.uix.boxlayout import BoxLayout
from kivy.garden.notification import Notification
Builder.load_string('''
<Notif>:
    Button:
        on_release: root.show_notification()
''')


class Notif(BoxLayout):
    def show_notification(self, *args):
        # Notification returns Thread it's run in
        print(Notification().open(
            title='Kivy Notification',
            message='Hello from the other side?',
            timeout=5,
            icon=resource_find('data/logo/kivy-icon-128.png')
        ))


class KivyNotification(App):
    def build(self):
        return Notif()


if __name__ == '__main__':
    KivyNotification().run()
```
