
class RedisSet:
    def __init__(self, redis, key, converter, content=None):
        self.key_ = key
        self.redis_ = redis
        self.converter_ = converter
        if content:
            self.reset(content)

    def __len__(self):
        return self.redis_.scard(self.key_)

    def __call__(self):
        return {
            self.converter_.to_value(v)
            for v in self.redis_.smembers(self.key_)
        }

    def __repr__(self):
        return str(self())

    def __str__(self):
        return str(self())

    def __contains__(self, key):
        return self.redis_.sismember(self.key_,
                                     self.converter_.from_value(key))

    def reset(self, value_list):
        self.redis_.delete(self.key_)
        self.redis_.sadd(self.key_,
                         *[self.converter_.from_value(v) for v in value_list])

    def add(self, value):
        self.redis_.sadd(self.key_, self.converter_.from_value(value))

    def pop(self):
        return self.converter_.to_value(self.redis_.spop(self.key_))
