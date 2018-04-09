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

import json

import requests


class AgentData:
    def __init__(self, ip):
        # TODO connection to stand, getting a params, setting it as attributes
        self.raw_data = requests.get('http://{}:5000/state'.format(ip))
        print(self.raw_data.content)
        data = json.loads(self.raw_data.content.decode('utf8'))

        self.last_activity = data['last_activity']
        self.tests = data['tests']
        self.ssh_clients = data['ssh_clients']

class AgentCommand:
    # TODO RPC for extended capabilities
    pass

if __name__ == '__main__':
    d = AgentData('127.0.0.1')
    print(d.last_activity)
    print(d.tests)
    print(d.ssh_clients)
