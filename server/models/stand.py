import uuid
from enum import Enum

from server.models.queue import Queue
from server.utils.characters import AVAIL_SMILE_UTF8, WARNING_SMILE_UTF8, CROSS_SMILE_UTF8, GEAR_SMILE_UTF8


class State(Enum):
    FREE   = 0,
    BUSY   = 1,
    ACTIVE = 2,


class Stand:
    def __init__(self, name, ip, login, password, platforms, alias, queue: Queue=None):
        self.name          = name
        self.ip            = ip
        self.login         = login
        self.password      = password
        self.platforms     = platforms
        self.alias         = alias
        self.user = None
        if queue:
            self.queue = queue

    def __repr__(self):
        # TODO return collected info by /1 cmd (example)
        data = self.collect_info()
        if data['state'] == State.FREE:
            return '{} *{}* \n' \
                   ' ``'.format(AVAIL_SMILE_UTF8, self.ip)
        elif data['state'] == State.BUSY:
            if data['tests']['is_running']:
                test_in_progress_str = '{0} TEST IN PROGRESS {0}\n' \
                                       '`Started at {1}\n' \
                                       'Current scenario {2}`\n\n'.format(GEAR_SMILE_UTF8, data['start_time'], data['scenario'])
            else:
                test_in_progress_str = ''

            return '{} *{}* at {},  last activity {}\n' \
                   'Queue:\n' \
                   '{}\n' \
                   '{}\n' \
                   'SSH sessions:\n' \
                   '{}'.format(CROSS_SMILE_UTF8, self.ip, self.user, data['last_activity'],
                               str(self.queue), test_in_progress_str, data['ssh_clients'])
        elif data['state'] == State.ACTIVE:
            pass

    def __str__(self):
        data = self.collect_info()
        '{0} *192.168.38.201 \[alias /1\]* @СергейЮсупов и еще 4\n`cl_all`\n\n'
        if self.state == State.FREE:
            return '{} *{}* /{}\n `{}`'.format(AVAIL_SMILE_UTF8, self.ip, self.alias, self.platforms)
        elif self.state == State.BUSY:
            return '{} *{}* /{} {} \n `{}`'.format(CROSS_SMILE_UTF8, self.ip, self.alias, str(self.user), self.platforms)
        elif self.state == State.ACTIVE:
            return '{} *{}* /{} \n `{}`'.format(CROSS_SMILE_UTF8, self.ip, self.alias, self.platforms)

    def collect_info(self):
        print(self.ip)
        info = {'state': State.FREE,
                'last_activity': '16:43',
                'tests': {'is_running': True, 'start_time': '14:32', 'scenario': 'modbus.xml'},
                'ssh_clients': 'autotest pts/5 16:33 (10.0.112.36)\n'
                               'autotest pts/2 13:42 (192.168.38.6)'}

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
