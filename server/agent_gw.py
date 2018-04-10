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

'''
http://192.168.38.211:9999/
{"scenario_name":"Base_Ncc_Crg","platform_name":"hw-1000-q6","start_time":"2018-04-10T12:14:03.074","steps_completed":0,"steps_remaining":3,"total_steps":3}
'''
class AgentData:
    def __init__(self, ip, timeout_sec=0.1):
        # TODO connection to stand, getting a params, setting it as attributes
        self.raw_data = requests.get('http://{}:5000/state'.format(ip), timeout=timeout_sec)
        # assert 200 == self.raw_data.status_code
        data = json.loads(self.raw_data.content.decode('utf8'))

        self.last_activity = data['last_activity']
        self.tests = data['tests']
        self.ssh_clients = data['ssh_clients']

        self.hw_tester_info = None

        try:
            self.hw_tester_info = requests.get('http://{}:9999'.format(ip), timeout=timeout_sec)
            data = json.loads(self.hw_tester_info.content.decode('utf8'))

            self.scenario_name = data['scenario_name']
            self.platform_name = data['platform_name']
            self.start_time = data['start_time']
            self.steps_completed = data['steps_completed']
            self.steps_remaining = data['steps_remaining']
            self.total_steps = data['total_steps']
        except:
            pass


class AgentCommand:
    # TODO RPC for extended capabilities
    pass

# if __name__ == '__main__':
#     d = AgentData('127.0.0.1')
#     print(d.last_activity)
#     print(d.tests)
#     print(d.ssh_clients)
