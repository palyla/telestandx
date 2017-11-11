from flask import Flask
from flask import json


app = Flask(__name__)


@app.route('/state')
def state():
    state = {
        'last_activity': '14:13',
        'ssh_clients': 'ssh clients',
        'tests': {'is_running': True, 'start_time': '12:45', 'scenario': 'modbus.xml'}
    }

    return json.dumps(state)


if __name__ == "__main__":
    app.run()
