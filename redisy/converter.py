import pickle
import json
import gzip


class Converter:
    CONVERT_METHOD_MAP = {
        'raw': 0,
        'json': 1,
        'pickle': 2,
        'gz': 3,
    }

    from_impl = [
        lambda x: x,
        lambda x: json.dumps(x),
        lambda x: pickle.dumps(x),
        lambda x: gzip.compress(pickle.dumps(x)),
    ]

    to_impl = [
        lambda x: x.decode,
        lambda x: json.loads(x),
        lambda x: pickle.loads(x),
        lambda x: gzip.decompress(pickle.loads(x)),
    ]

    def __init__(self, method='json'):
        self.method_ = self.CONVERT_METHOD_MAP[method]
        self.from_value = self.from_impl[self.method_]
        self.to_value = self.to_impl[self.method_]

