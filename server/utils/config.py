import os
from configparser import ConfigParser, ExtendedInterpolation


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Config:
    def __init__(self, conf_path=None):
        self.conf = ConfigParser(interpolation=ExtendedInterpolation())

        self.conf.add_section('sys')
        self_dir = os.path.dirname(os.path.abspath(__file__))
        self.conf['sys'] = {'script_dir' : self_dir}

        if conf_path:
            self.conf.read(conf_path)

    def __getitem__(self, item):
        return self.conf[item]

    def __iter__(self):
        return self.conf.__iter__()

    def sections(self, *args, **kwargs):
        return self.conf.sections()

    def keys(self):
        return self.conf.keys()

