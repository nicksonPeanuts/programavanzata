class DefaultDict:

    def __init__(self, default):
        self.d = {}
        self.default = default

    @classmethod
    def from_dict(cls, d, default):
        dd = cls(default)
        dd.d = d
        return dd

    def __contains__(self, k):
        return k in self.d

    def __getitem__(self, k):
        if k in self.d:
            return self.d[k]
        return self.default

    def __setitem__(self, k, v):
        self.d[k] = v

    def __delitem__(self, k):
        if k in self.d:
            del self.d[k]


class LinearFunction:

    def __init__(self, m, q):
        self.m = m
        self.q = q

    def __call__(self, x):
        return self.m * x + self.q

    def __str__(self):
        return f"{self.m}x + {self.q}"
