from rsakey import RSAPrivKey
from tools import int_from_bytes, int_to_bytes

def unpad(data):
    if ((data[0] != 0) or (data[1] != 2)):
        return None
    plen = data.find(0,2)
    return data[plen+1:]

def CryptImportKey(data):
    ret = RSAPrivKey(data)
    if not ret.valid:
        return None
    return ret

def CryptDecrypt(rsakey, data):
    data = int_from_bytes(data, "little")
    data = pow(data, rsakey.d, rsakey.N)
    data = int_to_bytes(data, rsakey.keylen, "big")
    return unpad(data)
