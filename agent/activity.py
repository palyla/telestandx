''' It does NOT support Wayland '''
import multiprocessing
from Xlib import display


class ProcessWatcher:
    '''
        git clone https://github.com/brendangregg/perf-tools.git
        cd perf-tools
        sudo ./execsnoop
    '''
    def __init__(self):
        pass

    def add_event(self, func):
        pass

class ActivityWatcher:

    def __init__(self):
        self.mouse_x = 0
        self.mouse_y = 0
        self.console_hashsum = 0

        # def setup_bashrc():
        #     with open()

    def is_mouse_changed(self, display_env=':0'):
        data = display.Display().screen().root.query_pointer()._data

        if self.mouse_x != data["root_x"] or self.mouse_y != data["root_y"]:
            self.mouse_x = data["root_x"]
            self.mouse_y = data["root_y"]
            print('New coordinates is ({}, {})'.format(self.mouse_x, self.mouse_y))
            return True

        return True

    def is_console_changed(self):
        ''' "PROMPT_COMMAND='history -a" must be in ~/.bashrc '''
        ''' export PROMPT_COMMAND="echo $('date') > ~/.bash_last_activity" '''



        return False


if __name__ == '__main__':
    activity = ActivityWatcher()
    activity.is_mouse_changed()
    activity.is_mouse_changed()
