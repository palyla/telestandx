''' It does NOT support Wayland '''
import multiprocessing
import os

from Xlib import display
from os import subprocess

class ProcessWatcher:
    '''
        git clone https://github.com/brendangregg/perf-tools.git
        cd perf-tools
        sudo ./execsnoop
    '''
    def __init__(self):
        self.events = list()
        self.proc = None
        self.stop = False

        def install_watcher(path):
            if not os.path.exists(path):

                os.mknod(path)
                os.system('cd {} && git clone https://github.com/brendangregg/perf-tools.git'.format(path))

            return os.path.join(path, 'perf-tools/execsnoop')

        self.elf_path = install_watcher('/opt/telestandx_agent_watcher')

    def add_event(self, handler):
        self.events.append(handler)

    def routine(self):
        self.proc = subprocess.Popen(self.elf_path, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while True:
            if self.stop:
                break
            line = self.proc.stdin.readline()
            for e in self.events:
                e(line)

    def stop(self):
        self.stop = True


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
