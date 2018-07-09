
class RedisList:
    def __init__(self, redis, key, converter, content=None):
        self.key_ = key
        self.redis_ = redis
        self.converter_ = converter
        if content:
            self.reset(content)

    def __len__(self):
        return self.redis_.llen(self.key_)

    def __getitem__(self, index):
        if type(index) is slice:
            start = index.start if index.start else 0
            stop = index.stop - 1 if index.stop else -1
            value = self.redis_.lrange(self.key_, start, stop)
            value = [self.converter_.to_value(v) for v in value]
        else:
            value = self.redis_.lindex(self.key_, index)
            if value is None:
                raise IndexError('list index out of range')
            value = self.converter_.to_value(value)
        return value

    def __setitem__(self, index, value):
        self.redis_.lset(self.key_, index, self.converter_.from_value(value))
        return value

    def __call__(self):
        return self[:]

    def __repr__(self):
        return str(self())

    def __str__(self):
        return str(self())

    def reset(self, value_list):
        self.redis_.delete(self.key_)
        self.redis_.rpush(self.key_,
                          *[self.converter_.from_value(v) for v in value_list])

    def append(self, value):
        self.redis_.rpushx(self.key_, self.converter_.from_value(value))

    def extend(self, value_list):
        self.redis_.rpush(self.key_,
                          *[self.converter_.from_value(v) for v in value_list])

    def pop(self, idx=-1):
        if idx == 0:
            return self.converter_.to_value(self.redis_.lpop(self.key_))
        else:
            return self.converter_.to_value(self.redis_.rpop(self.key_))
