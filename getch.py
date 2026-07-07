# From http://code.activestate.com/recipes/134892/
# Modified to support Android/Pydroid 3 (Termios bypass)

class _Getch:
    """Gets a single character from standard input.  Does not echo to the screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            import os
            if 'ru.iiec.pydroid3' in os.environ.get('PATH', '') or os.path.exists('/data/user/0/ru.iiec.pydroid3'):
                self.impl = _GetchAndroid()
            else:
                self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchAndroid:
    def __call__(self):
        try:
            ch = input()
            return ch[0] if ch else '\x00'
        except (KeyboardInterrupt, EOFError):
            return '\x00'



class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


getch = _Getch()
