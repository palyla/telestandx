import queue
from collections import deque

''' Храним только идетификаторы пользователей '''
class Queue(queue.Queue):
    def remove(self, obj):
        new_queue = deque()
        for i in self.queue:
            if i != obj:
                new_queue.append(obj)
        self.queue = new_queue

    def is_empty(self):
        pass

    def length(self):
        pass

    def head(self):
        if self.not_empty():
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
            msg += '{}. {}\n'.format(count, i)

        if msg:
            return msg
        else:
            return 'Empty'


if __name__ == '__main__':
    q = Queue()
    q.put(1)
    q.put(2)
    q.put(3)

    print(q)

    q.remove(1)

    print(q)