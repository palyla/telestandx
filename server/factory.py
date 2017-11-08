from server.utils.config import Config
from server.models.stand import Stand

# TODO queue factory
# TODO stand factory


class QueueFactory:
    @staticmethod
    def get():
        pass


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
                config[block]['platforms']
            )
        raise StopIteration
