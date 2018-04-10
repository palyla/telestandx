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

import socket
import requests
from enum import IntEnum

from server.models.message import StandInfoMessage, StandOverviewMessage
from server.models.users_queue import Queue
from server.agent_gw import AgentData
from server.utils.helper import print_exceptions


class State:
    class Status(IntEnum):
        UNKNOWN = -1
        FREE    = 0,
        BUSY    = 1,
        ACTIVE  = 2,

    def __init__(self, stand, connection_timeout_sec=1.5):
        self.stand = stand

        try:
            self.agent = AgentData(stand.ip, timeout_sec=connection_timeout_sec)
            self.last_activity = self.agent.last_activity
            self.tests = self.agent.tests
            self.ssh_clients = self.agent.ssh_clients
            self.is_connection_success = True
        except Exception as e:
            self.last_activity = 'unknown'
            self.tests = {'is_running': False}
            self.ssh_clients = {}
            self.is_connection_success = False

    @property
    def user(self):
        return self.stand.user

    @property
    def ip(self):
        return self.stand.ip

    @property
    def queue(self):
        return self.stand.queue

    @property
    def status(self):
        return self.stand.status

    @property
    def platforms(self):
        return self.stand.platforms

    @property
    def alias(self):
        return self.stand.alias


class Stand:
    def __init__(self, name, ip, login, password, platforms, alias, queue: Queue=None):
        self.name          = name
        self.ip            = ip
        self.login         = login
        self.password      = password
        self.platforms     = platforms
        self.alias         = alias
        self.status        = State.Status.FREE
        if queue:
            self.queue = queue
        else:
            self.queue = Queue()

    @print_exceptions
    def __repr__(self):
        return StandInfoMessage(self.state).message()

    @print_exceptions
    def __str__(self):
        return StandOverviewMessage(self.state).message()

    @property
    def state(self):
        return None

    @state.getter
    def state(self):
        st = State(self)
        if st.is_connection_success:
            self._check_users()
        else:
            self.status = State.Status.UNKNOWN
        return st

    def set_queue(self, queue):
        self.queue = queue

    @print_exceptions
    def new_user(self, user):
        if not self.queue.full() \
                and user not in self.queue.queue:

            self.queue.put(user)
            self.status = State.Status.BUSY
        if user in self.queue:
            pass
        else:
            self.status = State.Status.BUSY

    @print_exceptions
    def next_user(self):
        if not self.queue.empty() and not self.queue.full():
            self.queue.get()
            self.status = State.Status.BUSY
        else:
            self.status = State.Status.FREE

        self._check_users()

    def del_user(self, user_id):
        self.queue.remove(user_id)
        self._check_users()

    def _check_users(self):
        if self.queue.empty():
            self.status = State.Status.FREE

    @property
    def user(self):
        return None

    @user.getter
    def user(self):
        return self.queue.head()
