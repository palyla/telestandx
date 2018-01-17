import socket
import requests
from enum import IntEnum

from server.models.message import StandInfoMessage, StandOverviewMessage
from server.models.queue import Queue
from server.agent_gw import AgentData
from server.utils.helper import print_exceptions
from server.utils.characters import AVAIL_SMILE_UTF8, WARNING_SMILE_UTF8, CROSS_SMILE_UTF8, GEAR_SMILE_UTF8, \
    SLEEP_SMILE_UTF8


class State:
    class Status(IntEnum):
        UNKNOWN = -1
        FREE    = 0,
        BUSY    = 1,
        ACTIVE  = 2,

    def __init__(self, stand):
        self.stand = stand
        self.agent = AgentData(stand.ip)

    @property
    def last_activity(self):
        return self.agent.last_activity

    @property
    def tests(self):
        return self.agent.tests

    @property
    def ssh_clients(self):
        return self.agent.ssh_clients

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
    def queue(self):
        return self.stand.status

    @property
    def platforms(self):
        return self.stand.platforms

class Stand:
    def __init__(self, name, ip, login, password, platforms, alias, queue: Queue=None):
        self.name          = name
        self.ip            = ip
        self.login         = login
        self.password      = password
        self.platforms     = platforms
        self.alias         = alias
        self.user          = None
        self.status        = State.Status.FREE
        if queue:
            self.queue = queue

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
        try:
            socket.gethostbyaddr(self.ip)
            return State(self)
        except socket.herror:
            return None
        except requests.exceptions.ConnectionError as e:
            return None

    def set_queue(self, queue):
        self.queue = queue

    @print_exceptions
    def new_user(self, user):
        if not self.queue.empty() and user not in self.queue:
            self.queue._put(user)
        if user in self.queue:
            pass
        else:
            self.status = State.Status.BUSY
            self.user = user

    @print_exceptions
    def next_user(self):
        if not self.queue.empty():
            self.user = self.queue._get()
            self.status = State.Status.BUSY
        else:
            self.status = State.Status.FREE
            self.user = None

    def del_user(self, user):
        pass

    def current_user(self):
        return self.user
