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

import queue
from collections import deque


class Queue(queue.Queue):
    def remove(self, obj):
        is_removed = False
        new_queue = deque()
        for i in self.queue:
            if i != obj:
                new_queue.append(i)
                continue
            is_removed = True
        self.queue = new_queue
        if not is_removed:
            raise FileNotFoundError('User not in queue')

    def head(self):
        if not self.empty():
            for i in self.queue:
                return i

    def __iter__(self):
        return self.queue.__iter__()

    def __next__(self):
        return self.queue.__next__()

    def __str__(self):
        msg = ''
        count = 0
        for i in self.queue:
            count += 1
            msg += '{}. @{}\n'.format(count, i)

        if msg:
            return msg
        else:
            return ''
