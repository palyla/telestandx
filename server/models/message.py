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
import datetime

from server.utils.characters import Emoji


class Message:
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class ProgressBarMessage:
    def __init__(self, completed, total, completed_symbol='▓', way_symbol='░', length=50, show_percent=False):
        percent = int((completed * 100) / total)
        completed_symbols_num = int((length * percent) / 100)
        way_symbols_num = int(length - completed_symbols_num)
        self.percent = percent

        if show_percent:
            self.msg = '{}{} {}%'.format(completed_symbol * completed_symbols_num, way_symbol * way_symbols_num, percent)
        else:
            self.msg = '{}{}'.format(completed_symbol * completed_symbols_num, way_symbol * way_symbols_num)

    def message(self):
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
        return '{}'.format(self.state.queue)

    @property
    def test_progress(self):
        if hasattr(self.state, 'scenario_name') and hasattr(self.state, 'tests') and self.state.tests['is_running']:
            start_time = datetime.datetime.strptime(self.state.start_time.split('.')[0], '%Y-%m-%dT%H:%M:%S').strftime('%H:%M')
            progress_length = 35
            progress = ProgressBarMessage(self.state.steps_completed, self.state.total_steps, length=progress_length, show_percent=True)

            msg = '{0} TEST IN PROGRESS {0}\n' \
            '`Started at {4}, platform {1}, scenario {2}, config {3}`\n' \
            '{5}\n'.format(Emoji.UTF8.GEAR, self.state.platform_name, self.state.scenario_name,
                           self.state.tests['scenario'], start_time, progress.message())

            return msg

        elif hasattr(self.state, 'tests') and self.state.tests['is_running']:
            msg = '{0} TEST IN PROGRESS {0}\n' \
            '`Started at {1}\n' \
            'Current scenario: {2}`\n'.format(Emoji.UTF8.GEAR, self.state.tests['start_time'], self.state.tests['scenario'])

            if self.state.tests['is_alive']:
                alert_msg = '{0} TESTS IS DOWN!!! {0}\n'.format(Emoji.UTF8.SCULL)
                '{} {}'.format(msg, alert_msg)

            return msg

        return ''

    @property
    def ssh_clients(self):
        if '{}' == self.state.ssh_clients:
            return ''

        msg = 'Logged in: \n'
        count = 0
        for tty, host in self.state.ssh_clients.items():
            count += 1
            msg += '``` {}. {} {}```\n'.format(count, tty, host)

        if count == 0:
            return ''
        # if hasattr(self.state, 'ssh_clients'):
        #     return 'SSH sessions:\n {}'.format(self.state.ssh_clients)
        # else:
        #     return 'SSH sessions: unknown'
        return msg

    def message(self):
        return '{}{}{}{}'.format(self.header,
                                 self.queue,
                                 self.test_progress,
                                 self.ssh_clients)
        # return '{}{}{}'.format(self.header,
        #                          self.queue,
        #                          self.test_progress)

class StandShortInfoMessage:
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

        return '{} *{}* at @{},  last activity {}\n'.format(emoji, self.state.ip, self.state.user, 'unknown')

    @property
    def queue(self):
        return '{}'.format(self.state.queue)

    def message(self):
        return '{}{}'.format(self.header, self.queue)


class MessageDataCorrupted(Exception):
    ''' Raises then data corrupted or not exists '''