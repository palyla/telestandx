from queue import Queue as StdQueue


class Queue(StdQueue):
    def remove(self, obj):
        for i in self.queue:
            print(i)

    def is_empty(self):
        pass

    def length(self):
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


if __name__ == '__main__':
    q = Queue()
    q.put('Zero')
    q.put('One')
    q.put('Two')
    q.put('Three')
    q.put('Four')
    q.put('Five')
    q.put('Six')

    print(q)