from server.utils.config import Config
from server.models.stand import Stand

# TODO queue factory
# TODO stand factory


class StandFactory:
    def __init__(self):
        self.config = Config(conf_path='../stands.ini')

    def get_one(self):
        for block in self.config:
            yield Stand(
                block['name'],
                block['ip'],
                block['login'],
                block['password'],
                block['platforms']
            )

    def __next__(self):
        return self.get_one()

    def __iter__(self):
        return self
