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

from server.utils.config import Config
from server.models.stand import Stand
from server.models.users_queue import Queue


class QueueFactory:

    @staticmethod
    def get_one():
        return Queue()


class StandFactory:
    @staticmethod
    def get():
        config = Config(conf_path='stands.ini')
        for block in config:
            if 'sys' in block or 'DEFAULT' in block:
                continue
            yield Stand(
                config[block]['name'],
                config[block]['ip'],
                config[block]['login'],
                config[block]['password'],
                config[block]['platforms'],
                config[block]['alias']
            )
        raise StopIteration
