import heapq

import itertools


class Queue:
    def __init__(self):
        self.pq = []
        self.entry_finder = {}
        self.REMOVED = '<removed-obj>'
        self.counter = itertools.count()

    def push(self, obj, priority=0):
        if obj in self.entry_finder:
            self.remove(obj)
        count = next(self.counter)
        entry = [priority, count, obj]
        self.entry_finder[obj] = entry
        heapq.heappush(self.pq, entry)

    def remove(self, obj):
        entry = self.entry_finder.pop(obj)
        entry[-1] = self.REMOVED

    def pop(self):
        while self.pq:
            priority, count, obj = heapq.heappop(self.pq)
            if obj is not self.REMOVED:
                del self.entry_finder[obj]
                return obj
        raise KeyError('pop from an empty priority queue')

    def is_empty(self):
        if self.pq:
            return True
        else:
            return False

    # def __iter__(self):
    #     return self.queue.__iter__()
    #
    # def __next__(self):
    #     return self.queue.__next__()

    def __str__(self):
        msg = ''
        count = 0
        for i in self.queue:
            count += 1
            msg += '{}. {}\n'.format(count, i)

        if msg:
            return msg
        else:
            return 'Empty'
