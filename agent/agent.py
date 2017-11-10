import flask
from flask import Flask
from flask import json

from server.models.stand import State


app = Flask(__name__)


@app.route('/state')
def hello():
    state = {
        'status': State.Status.FREE,
        'last_activity': '14:13',
        'ssh_clients': 'ssh_clients',
        'tests': {'is_running': True, 'start_time': '12:45', 'scenario': 'modbus.xml'}
    }

    return json.dumps(state)


if __name__ == "__main__":
    app.run()
