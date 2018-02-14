'''
The telestandx is a Telegram bot for optimize team work with hardware stands running by Linux.
Copyright (C) 2017  Sedlyarskiy Alexey

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
'''

''' It does NOT support Wayland '''
import multiprocessing
import os
from Xlib import display


class ProcessWatcher:
    '''
        git clone https://github.com/brendangregg/perf-tools.git
        cd perf-tools
        sudo ./execsnoop
    '''
    def __init__(self, pipe):
        self.events = list()
        self.pipe = pipe
        self.proc = None
        self.stop = False

    def add_event(self, handler):
        self.events.append(handler)

    def routine(self):
        self.proc = os.subprocess.Popen('execsnoop', stdout=os.subprocess.PIPE, stderr=os.subprocess.STDOUT)
        while True:
            if self.stop:
                break
            line = self.proc.stdin.readline()
            for e in self.events:
                res = e(line)
                if res:
                    self.pipe.send(res)

    def stop(self):
        self.stop = True


class ActivityWatcher:

    def __init__(self):
        self.mouse_x = 0
        self.mouse_y = 0

    def is_mouse_changed(self, display_env=':0'):
        data = display.Display().screen().root.query_pointer()._data

        if self.mouse_x != data["root_x"] or self.mouse_y != data["root_y"]:
            self.mouse_x = data["root_x"]
            self.mouse_y = data["root_y"]
            print('New coordinates is ({}, {})'.format(self.mouse_x, self.mouse_y))
            return True

        return True


if __name__ == '__main__':
    activity = ActivityWatcher()
    activity.is_mouse_changed()
    activity.is_mouse_changed()
