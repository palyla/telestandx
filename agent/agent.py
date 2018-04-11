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
import threading

import time
import os
import datetime
import multiprocessing
import psutil
from Xlib import display
from flask import Flask
from flask import json

# pip3 install Xlib python-telegram-bot flask psutil


class ActivityWatcher:
    def __init__(self):
        self.events = list()

    def add_event(self, handler):
        self.events.append(handler)

    def routine(self, store_to):
        while True:
            time.sleep(1)
            tmp = dict()
            for event in self.events:
                res = event()
                if res:
                    tmp[event.__name__] = res

            store_to.clear()
            store_to.update(tmp)


def monitoring(state):
    last_activity = None

    def upd_proc():
        global last_activity
        list_of_activity_markers = ['ls', 'cd', 'pwd']
        list_of_tests_markers = ['java', 'perl']

        procs = {p.pid: p.info for p in psutil.process_iter(attrs=['exe', 'cmdline', 'create_time'])}
        msg = {}

        for pid, proc in procs.items():
            if not proc['cmdline'] or not proc['exe']:
                continue

            for marker in list_of_activity_markers:
                if marker in proc['cmdline']:
                    last_activity = time.time()
            for marker in list_of_tests_markers:
                if marker in proc['cmdline'][0]:
                    msg.update({marker: proc})

        if last_activity:
            msg['last_tty_activity'] = last_activity
        return msg

    _mouse_x = None
    _mouse_y = None
    def upd_mouse(display_env=':0'):
        global last_activity
        nonlocal _mouse_x
        nonlocal _mouse_y
        data = display.Display(display=display_env).screen().root.query_pointer()._data
        msg = {}

        if _mouse_x != data["root_x"] or _mouse_y != data["root_y"]:
            msg['mouse_x'] = _mouse_x = data["root_x"]
            msg['mouse_y'] = _mouse_y = data["root_y"]
            last_activity = time.time()

            if last_activity:
                msg['last_mouse_activity'] = last_activity
            return msg

    def upd_users():
        users = dict()
        for usr in psutil.users():
            if 'localhost' not in usr[2]:
                users[usr[1]] = usr[2]
        return users

    act = ActivityWatcher()
    act.add_event(upd_mouse)
    act.add_event(upd_proc)
    act.add_event(upd_users)
    act.routine(state)


def networking(state):
    app = Flask(__name__)

    @app.route('/state')
    def state_query():
        global state

        if 'upd_proc' in state:
            if 'java' in state['upd_proc'] and 'hwTester.jar' in \
                    state['upd_proc']['java']['cmdline'][2]:
                start_timestamp = datetime.datetime.fromtimestamp(state['upd_proc']['perl']['create_time']).time().strftime('%H:%M')
                current_scenario = state['upd_proc']['java']['cmdline'][4]
                tests = {'is_running': True, 'is_alive': True, 'start_time': start_timestamp,
                         'scenario': os.path.basename(current_scenario)}
            else:
                tests = {'is_running': False}
        else:
            tests = {'is_running': False}

        if 'upd_users' in state:
            ssh_clients = state['upd_users']
        else:
            ssh_clients = '{}'

        last_tty_activity = None
        if 'upd_proc' in state:
            if 'last_tty_activity' in state['upd_proc']:
                last_tty_activity = datetime.datetime.fromtimestamp(float(state['upd_proc']['last_tty_activity'])).time()
        last_mouse_activity = None
        if 'upd_mouse' in state:
            if 'last_mouse_activity' in state['upd_proc']:
                last_mouse_activity = datetime.datetime.fromtimestamp(float(state['upd_proc']['last_mouse_activity'])).time()

        activity = 'unknown'
        if last_tty_activity and last_mouse_activity:
            if last_tty_activity >= last_mouse_activity:
                activity = last_tty_activity
            else:
                activity = last_mouse_activity
        elif last_tty_activity:
            activity = last_tty_activity
        elif last_mouse_activity:
            activity = last_mouse_activity

        ret_state = {
            'last_activity': activity.strftime('%H:%M'),
            'ssh_clients': ssh_clients,
            'tests': tests
        }

        return json.dumps(ret_state)

    app.run(host='0.0.0.0', debug=False, use_reloader=False)


if __name__ == "__main__":
    with multiprocessing.Manager() as mgr:
        state = mgr.dict()

        mon_proc = multiprocessing.Process(target=monitoring, args=(state,))
        net_proc = multiprocessing.Process(target=networking, args=(state,))

        mon_proc.start()
        time.sleep(1)
        net_proc.start()
        net_proc.join()

        mon_proc.terminate()
        mon_proc.join()
