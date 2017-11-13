from queue import PriorityQueue
import itertools


class Queue(PriorityQueue):
    def remove(self):
        # TODO implement by heapq. (self.queue is heapq)
        pass

    def __iter__(self):
        return self.queue.__iter__()

    def __next__(self):
        return self.queue.__next__()

    def __str__(self):
        msg = ''
        count = 0
        for i in self.queue:
            count += 1
            msg += '{}. {}\n'.format(count, i[1])

        if msg:
            return msg
        else:
            return 'Empty'
