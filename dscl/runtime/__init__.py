class KV:
    def __init__(self, k,v):
        self.key=k
        self.value=v
    def __repr__(self):
        return f"{self.key}={self.value}"

class Table:
    def __init__(self, *i, **k):
        self._k=k
        self._i=list(i)
        self._ch=len(i)
        self._chl=len(k)
        self.length=self._ch+self._chl

        self._kiter=[KV(k,v) for k, v in self._k.items()]

    def __len__(self):
        return self.length
    def __getitem__(self, i):
        if len(self._i)<i:
            return self._i[i]
        return self._k[i]
    def __setitem__(self, i, v):
        if len(self._i)<i:
            self._i[i]=v
        else:
            self._k[i]=v
            self._kiter=[KV(k,v) for k, v in self._k.items()]

    def __delitem__(self, i):
        if len(self._i)<i:
            del self._i[i]
        else:
            del self._k[i]
            self._kiter=[KV(k,v) for k, v in self._k.items()]

    def __iter__(self):
        return iter(self._iters)
    @property
    def _iters(self):
        return self._i+self._kiter
    def append(self, i):
        self._i.append(i)
        self._ch+=1
        self.length+=1
    def pop(self, index=-1):
        res = self._i.pop()
        self.length-=1
        self._ch-=1
        return res
    def __repr__(self):
        return "["+",".join(map(repr, self))+"]"

UserDatabase=Table
