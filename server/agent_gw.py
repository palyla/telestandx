# from server.models.stand import State


class AgentData:
    def __init__(self, ip):
        # TODO connection to stand, getting a params, setting it as attributes
        self.status = 0
        self.last_activity = '14:13'
        self.tests = {'is_running': '', 'start_time': '', 'scenario': ''}
        self.ssh_clients = 'ssh'


class AgentCommand:
    # TODO RPC for extended capabilities
    pass
