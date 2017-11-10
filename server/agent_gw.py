from server.models.stand import State


class AgentData:
    def __init__(self, ip):
        # TODO connection to stand, getting a params, setting it as attributes
        self.status = State.Status.FREE
        self.last_activity = '14:13'
        self.tests = {'is_running': '', 'start_time': '', 'scenario': ''}
        self.ssh_clients = State.Status.FREE


class AgentCommand:
    # TODO RPC for extended capabilities
    pass
