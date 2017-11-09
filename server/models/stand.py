import uuid
from enum import Enum

from queue import Queue
from server.utils.characters import AVAIL_SMILE_UTF8, WARNING_SMILE_UTF8, CROSS_SMILE_UTF8


class State(Enum):
    FREE   = 0,
    BUSY   = 1,
    ACTIVE = 2,


class Stand:
    def __init__(self, name, ip, login, password, platforms, alias, queue: Queue=None):
        self.name      = name
        self.ip        = ip
        self.login     = login
        self.password  = password
        self.platforms = platforms
        self.alias     = alias
        self.state     = State.FREE

        if queue:
            self.queue = queue

    def __repr__(self):
        # TODO return collected info by /1 cmd (example)
        return uuid.uuid4().hex

    def __str__(self):
        '{0} *192.168.38.201 \[alias /1\]* @СергейЮсупов и еще 4\n`cl_all`\n\n'
        if self.state == State.FREE:
            return '{} *{}* /{}\n `{}`'.format(AVAIL_SMILE_UTF8, self.ip, self.alias, self.platforms)
        elif self.state == State.BUSY:
            return '{} *{}* /{} {} \n `{}`'.format(CROSS_SMILE_UTF8, self.ip, self.alias, str(self.user), self.platforms)
        elif self.state == State.ACTIVE:
            return '{} *{}* /{} \n `{}`'.format(CROSS_SMILE_UTF8, self.ip, self.alias, self.platforms)

    def collect_info(self):
        # last activity
        # queue
        # tests is going on?
        # current ssh sessions
        info = {}





        return info


    def set_queue(self, queue):
        self.queue = queue

    def new_user(self, user):
        if not self.queue.empty():
            self.queue.put(user)
        else:
            self.user = user

    def next_user(self):
        if not self.queue.empty():
            self.user = self.queue.get()
        else:
            self.user = None

    def current_user(self):
        return self.user
