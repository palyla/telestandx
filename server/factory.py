from server.utils.config import Config
from server.models.stand import Stand
from server.models.queue import Queue


class QueueFactory:

    @staticmethod
    def get_one():
        return Queue()


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
                config[block]['platforms'],
                config[block]['alias']
            )
        raise StopIteration
