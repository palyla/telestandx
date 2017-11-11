import json

import requests


class AgentData:
    def __init__(self, ip):
        # TODO connection to stand, getting a params, setting it as attributes
        raw_data = requests.get('http://{}:5000/state'.format(ip))
        data = json.loads(raw_data.content.decode('utf8'))
        self.status = data['status']
        self.last_activity = data['last_activity']
        # {'is_running': '', 'start_time': '', 'scenario': ''}
        self.tests = data['tests']
        self.ssh_clients = data['ssh_clients']

class AgentCommand:
    # TODO RPC for extended capabilities
    pass
