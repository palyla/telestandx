


class Queue:
    def __init__(self):
        self.members = list()

    def pop(self, obj=None):
        if not obj:
            return self.members.pop()
        else:
            for member in self.members:
                if obj is member:
                    return member

    def push(self, obj):
        self.members.append(obj)

    def __getitem__(self, item):
        return self.members[item]

    def __iter__(self):
        return self.members.__iter__()

    def __next__(self):
        return self.members.__next__()
