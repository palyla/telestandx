import uuid

from queue import Queue


class Stand:
    def __init__(self, name, ip, login, password, platforms, alias, queue: Queue=None):
        self.name       = name
        self.ip         = ip
        self.login      = login
        self.password   = password
        self.platforms  = platforms.split()
        self.alias      = alias

        if queue:
            self.queue  = queue

    def __str__(self):
        return uuid.uuid4().hex

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
