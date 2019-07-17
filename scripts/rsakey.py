import struct
from tools import int_from_bytes

def import_int(b):
    return int_from_bytes(b, "little")

class Data:
    def __init__(self, data):
        self.__data = data

    def pop(self, n):
        ret = self.__data[:n]
        self.__data = self.__data[n:]
        return ret
class RSAPubKey:

    def __init__(self, data):
        data = Data(data)
        blob_header = struct.unpack("<BBHI", data.pop(8))
        pub_key = struct.unpack("<III", data.pop(12))
        self.keylen = pub_key[1]//8
        self.subkeylen = (self.keylen+1)//2
        self.N = import_int(data.pop(self.keylen))
        self.e = 0x10001

    @property
    def valid(self):
        return (self.N == self.p * self.q)

class RSAPrivKey:
    def __init__(self, data):
        data = Data(data)
        blob_header = struct.unpack("<BBHI", data.pop(8))
        pub_key = struct.unpack("<III", data.pop(12))
        self.keylen = pub_key[1]//8
        self.subkeylen = (self.keylen+1)//2
        self.N = import_int(data.pop(self.keylen))
        self.p = import_int(data.pop(self.subkeylen))
        self.q = import_int(data.pop(self.subkeylen))
        self.dP = import_int(data.pop(self.subkeylen))
        self.dQ = import_int(data.pop(self.subkeylen))
        self.iQ = import_int(data.pop(self.subkeylen))
        self.d = import_int(data.pop(self.keylen))
        #self.phi = gmpy2.lcm(self.p-1,self.q-1)
        self.e = 0x10001

    @property
    def valid(self):
        return (self.N == self.p * self.q)
