
class RedisHash:
    def __init__(self, redis, key, converter, content=None):
        self.key_ = key
        self.redis_ = redis
        self.converter_ = converter
        if content:
            self.reset(content)

    def __len__(self):
        return self.redis_.hlen(self.key_)

    def __getitem__(self, key):
        value = self.redis_.hget(self.key_, self.converter_.from_value(key))
        if value is None:
            raise KeyError(str(key))
        value = self.converter_.to_value(value)
        return value

    def __setitem__(self, key, value):
        self.redis_.hset(self.key_, self.converter_.from_value(key),
                         self.converter_.from_value(value))
        return value

    def __call__(self):
        return self.items()

    def __repr__(self):
        return str(self())

    def __str__(self):
        return str(self())

    def __contains__(self, key):
        return self.redis_.hexists(self.key_, self.converter_.from_value(key))

    def __delitem__(self, key):
        self.redis_.hdel(self.key_, self.converter_.from_value(key))

    def reset(self, value_dict):
        self.redis_.delete(self.key_)
        self.redis_.hmset(
            self.key_, {
                self.converter_.from_value(k): self.converter_.from_value(v)
                for k, v in value_dict.items()
            })

    def items(self):
        return {
            self.converter_.to_value(k): self.converter_.to_value(v)
            for k, v in self.redis_.hgetall(self.key_).items()
        }

    def keys(self):
        return [
            self.converter_.to_value(k) for k in self.redis_.hkeys(self.key_)
        ]

    def values(self):
        return [
            self.converter_.to_value(v) for v in self.redis_.hvals(self.key_)
        ]

    def pop(self, key):
        value = self[key]
        self.__delitem__(key)
        return value


