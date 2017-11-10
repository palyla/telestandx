from enum import IntEnum

from server.models.queue import Queue
from server.agent_gw import AgentData
from server.utils.characters import AVAIL_SMILE_UTF8, WARNING_SMILE_UTF8, CROSS_SMILE_UTF8, GEAR_SMILE_UTF8


class State:
    class Status(IntEnum):
        FREE   = 0,
        BUSY   = 1,
        ACTIVE = 2,

    def __init__(self, stand):
        self.agent = AgentData(stand.ip)

    @property
    def status(self):
        return self.agent.status

    @property
    def last_activity(self):
        return self.agent.last_activity

    @property
    def tests(self):
        return self.agent.tests

    @property
    def ssh_clients(self):
        return self.agent.ssh_clients


class Stand:
    def __init__(self, name, ip, login, password, platforms, alias, queue: Queue=None):
        self.name          = name
        self.ip            = ip
        self.login         = login
        self.password      = password
        self.platforms     = platforms
        self.alias         = alias
        self.user          = None
        if queue:
            self.queue = queue

    def __repr__(self):
        state = self.state
        if state.status == State.Status.FREE:
            return '{} *{}* at {},  last activity {}\n' \
                   'Queue:\n' \
                   '{}\n\n' \
                   'SSH sessions:\n' \
                   '{}'.format(AVAIL_SMILE_UTF8, self.ip, self.user, state.last_activity,
                               str(self.queue), state.ssh_clients)
        elif state.status == State.Status.BUSY:
            if state.tests['is_running']:
                test_in_progress_str = '{0} TEST IN PROGRESS {0}\n' \
                                       '`Started at {1}\n' \
                                       'Current scenario {2}`'.format(GEAR_SMILE_UTF8, state.tests['start_time'], state.tests['scenario'])
            else:
                test_in_progress_str = ''

            return '{} *{}* at {},  last activity {}\n' \
                   'Queue:\n' \
                   '{}\n\n' \
                   '{}\n\n' \
                   'SSH sessions:\n' \
                   '{}'.format(CROSS_SMILE_UTF8, self.ip, self.user, state.last_activity,
                               str(self.queue), test_in_progress_str, state.ssh_clients)
        elif state.status == State.Status.ACTIVE:
            if state.tests['is_running']:
                test_in_progress_str = '{0} TEST IN PROGRESS {0}\n' \
                                       '`Started at {1}\n' \
                                       'Current scenario {2}`\n'.format(GEAR_SMILE_UTF8, state.tests['start_time'], state.tests['scenario'])
            else:
                test_in_progress_str = ''

            return '{} *{}* at {},  last activity {}\n' \
                   'Queue:\n' \
                   '{}\n' \
                   '{}\n' \
                   'SSH sessions:\n' \
                   '{}'.format(WARNING_SMILE_UTF8, self.ip, self.user, state.last_activity,
                               str(self.queue), test_in_progress_str, state.ssh_clients)

    def __str__(self):
        state = self.state
        if state.status == State.Status.FREE:
            return '{} *{}* /{}\n `{}`'.format(AVAIL_SMILE_UTF8, self.ip, self.alias, self.platforms)
        elif state.status == State.Status.BUSY:
            return '{} *{}* /{} {} \n `{}`'.format(CROSS_SMILE_UTF8, self.ip, self.alias, '@user', self.platforms)
        elif state.status == State.Status.ACTIVE:
            return '{} *{}* /{} \n `{}`'.format(WARNING_SMILE_UTF8, self.ip, self.alias, self.platforms)

    @property
    def state(self):
        return None

    @state.getter
    def state(self):
        return State(self)

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
