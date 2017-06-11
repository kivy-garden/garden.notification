from kivy.utils import platform
from subprocess import check_output

# platform dependent imports
if platform == 'win':
    import ctypes
    import win32gui
    from win32con import (
        SW_HIDE, SW_SHOW,
        GWL_EXSTYLE, WS_EX_TOOLWINDOW
    )


def sys_resolution():
    # waiting for https://github.com/kivy/plyer/pull/201
    if platform == 'win':
        u32 = ctypes.windll.user32
        RESOLUTION = {
            'x': u32.GetSystemMetrics(0),
            'y': u32.GetSystemMetrics(1)
        }
    elif platform == 'linux':
        o = check_output('xrandr')
        start = o.find('current') + 7
        end = o.find(', maximum')
        res = [int(n) for n in o[start:end].split('x')]
        RESOLUTION = {
            'x': res[0],
            'y': res[1]
        }
    elif platform == 'osx':
        o = check_output(['system_profiler', 'SPDisplaysDataType'])
        start = o.find('Resolution: ')
        end = o.find('\n', start=start)
        o = o[start:end].strip().split(' ')
        RESOLUTION = {
            'x': int(o[1]),
            'y': int(o[3])
        }
    else:
        raise NotImplementedError("Not a desktop platform!")
    return RESOLUTION

def taskbar():
    if platform == 'win':
        # example:
        # right side  x>0  y=0    (1474,   0, 1536, 864)
        # left side   x=0  y<R/2  (   0,   0,   62, 864)
        # top side    x=0  y=0    (   0,   0, 1536,  27)
        # bot side    x=0  y>R/2  (   0, 837, 1536, 864)

        # get resolution to get taskbar position
        res = sys_resolution()

        # get taskbar rectangle
        handle = win32gui.FindWindow("Shell_traywnd", None)
        left, top, right, bottom = win32gui.GetWindowRect(handle)

        x = y = 0
        width, height = res

        if left:
            pos = 'right'
            x = left
            width = right - left
        elif right < res['y'] / 2.0:
            pos = 'left'
            width = right
        elif right > res['y'] / 2.0 and not top:
            pos = 'top'
            height = bottom
        elif right > res['y'] / 2.0 and top:
            pos = 'bottom'
            y = top
            height = bottom - top
    else:
        x, y, width, height, pos = (0, 0, 0, 0, '')

    return {
        'x': x, 'y': y,
        'width': width, 'height': height,
        'pos': pos
    }
