import uuid

from server.models.queue import Queue


class Stand:
    def __init__(self, name, ip, login, password, platforms, alias=None, queue: Queue=None):
        self.name       = name
        self.ip         = ip
        self.login      = login
        self.password   = password
        self.platforms  = platforms.split()
        if alias:
            self.alias  = alias

        if queue:
            self.queue  = queue

    def __str__(self):
        return uuid.uuid4()
