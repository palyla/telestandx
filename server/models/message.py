from server.utils.characters import Emoji


class Message:
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class StandOverviewMessage:
    def __init__(self, state):
        self.state = state

    def __str__(self):
        return self.message()

    @property
    def header(self):
        from server.models.stand import State
        emoji = 'BUG'

        if self.state.status is None \
                or self.state.status == State.Status.UNKNOWN:
            emoji = Emoji.UTF8.SLEEP
        elif self.state.status == State.Status.FREE:
            emoji = Emoji.UTF8.CHECK_MARK
        elif self.state.status == State.Status.ACTIVE:
            emoji = Emoji.UTF8.WARNING
        elif self.state.status == State.Status.BUSY:
            return '{} *{}* /{} {} \n `{}`'.format(Emoji.UTF8.CROSS, self.state.ip, self.state.alias, self.state.user, self.state.platforms)

        return '{} *{}* /{}\n `{}`'.format(emoji, self.state.ip, self.state.alias, self.state.platforms)

    def message(self):
        return '{}'.format(self.header)


class StandInfoMessage:
    def __init__(self, state):
        self.state = state

    def __str__(self):
        return self.message()

    @property
    def header(self):
        from server.models.stand import State
        emoji = 'BUG'

        if self.state.status is None \
                or self.state.status == State.Status.UNKNOWN:
            return '{} *{}* at @{},  last activity unknown\n'.format(Emoji.UTF8.SLEEP, self.state.ip, self.state.user)
        elif self.state.status == State.Status.FREE:
            emoji = Emoji.UTF8.CHECK_MARK
        elif self.state.status == State.Status.BUSY:
            emoji = Emoji.UTF8.CROSS
        elif self.state.status == State.Status.ACTIVE:
            emoji = Emoji.UTF8.WARNING

        return '{} *{}* at @{},  last activity {}\n'.format(emoji, self.state.ip, self.state.user, self.state.last_activity)

    @property
    def queue(self):
        return 'Queue: empty\n'

    @property
    def test_progress(self):

        if self.state.tests['is_running']:
            msg = '{0} TEST IN PROGRESS {0}\n' \
            '`Started at {1}\n' \
            'Current scenario {2}`\n'.format(Emoji.UTF8.GEAR, self.state.tests['start_time'], self.state.tests['scenario'])

            if self.state.tests['is_alive']:
                alert_msg = '{0} TESTS IS DOWN!!! {0}\n'.format(Emoji.UTF8.SCULL)
                '{} {}'.format(msg, alert_msg)

            return msg

        return ''

    @property
    def ssh_clients(self):
        return 'SSH sessions:\n {}'.format(self.state.ssh_clients)

    def message(self):
        return '{}{}\n{}\n{}'.format(self.header,
                                 self.queue,
                                 self.test_progress,
                                 self.ssh_clients)


class MessageDataCorrupted(Exception):
    ''' Raises then data corrupted or not exists '''