try:
    from redis import Redis
except ImportError:
    Redis = object
from .converter import Converter
from .redis_list import RedisList
from .redis_set import RedisSet
from .redis_hash import RedisHash


class Redisy(Redis):
    def __init__(self, **args):
        super(Redisy, self).__init__(**args)
        self.converter_ = Converter('json')

    def __getitem__(self, key):
        t = self.type(key)
        if t == b'string':
            return self.converter_.to_value(self.get(key))
        elif t == b'list':
            return RedisList(self, key, self.converter_)
        elif t == b'set':
            return RedisSet(self, key, self.converter_)
        elif t == b'hash':
            return RedisHash(self, key, self.converter_)
        elif t == b'none':
            return None

    def __setitem__(self, key, value):
        t = type(value)
        if t is list:
            RedisList(self, key, self.converter_, value)
        elif t is set:
            RedisSet(self, key, self.converter_, value)
        elif t is dict:
            RedisHash(self, key, self.converter_, value)
        else:
            self.set(key, self.converter_.from_value(value))
