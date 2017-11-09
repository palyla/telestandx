import queue


class Queue(queue.Queue):
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
