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
            self.conf.read(conf_path, encoding='utf8')

    def __getitem__(self, item):
        return self.conf[item]

    def __iter__(self):
        return self.conf.__iter__()

    def sections(self, *args, **kwargs):
        return self.conf.sections()

    def keys(self):
        return self.conf.keys()

