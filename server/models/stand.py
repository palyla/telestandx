from server.models.queue import Queue


class Stand:
    def __init__(self, name, ip, login, password, platforms, queue: Queue=None):
        self.name       = name
        self.ip         = ip
        self.login      = login
        self.password   = password
        self.platforms  = platforms.split()

        if queue:
            self.queue = queue
