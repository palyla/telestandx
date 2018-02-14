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

from flask import Flask
from flask import json


app = Flask(__name__)


@app.route('/state')
def state():
    state = {
        'last_activity': 'unknown',
        'ssh_clients': 'unknown',
        'is_alive': True,
        'tests': {'is_running': False, 'is_alive': True, 'start_time': '12:45', 'scenario': 'modbus.xml'}
    }

    return json.dumps(state)


if __name__ == "__main__":
    app.run()
