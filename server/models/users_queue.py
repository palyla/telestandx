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
