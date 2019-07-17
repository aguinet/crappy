import sys
from Crypto.Cipher import Salsa20
from wincrypt import CryptImportKey, CryptDecrypt

if len(sys.argv) <= 2:
    print("Usage: %s rsa_user_private_file encrypted_file" % sys.argv[0], file=sys.stderr)
    sys.exit(1)

privUserRsaFile, fencrname = sys.argv[1], sys.argv[2]

privUserRsa = open(privUserRsaFile,"rb").read()
privUserRsa = CryptImportKey(privUserRsa)
assert(privUserRsa)

padding_end = 28
pos_nonce = padding_end+256
pos_key   = padding_end+256*2

fencr = open(fencrname,"rb")
fencr.seek(-padding_end, 2)
pad = fencr.read(padding_end)

if (pad[20:] != bytes.fromhex("1829899381820300")):
    print("[X] This file doesn't seem to be encrypted with Gandcrab 5.2!", file=sys.stderr)
    sys.exit(1)

fdecrname = ".".join(fencrname.split(".")[:-1])
fdecr = open(fdecrname,"wb")

fencr.seek(-pos_nonce, 2)
encrNonceData = fencr.read(256)
nonceData = CryptDecrypt(privUserRsa, encrNonceData)
nonce = nonceData[:8]

keyData = fencr.seek(-pos_key, 2)
encrKeyData = fencr.read(256)
keyData = CryptDecrypt(privUserRsa, encrKeyData)
key = keyData[:32]

print("[+] Salsa20 key = %s" % key.hex())
print("[+] Salsa20 nonce = %s" % nonce.hex())

fencr.seek(0, 2)
size = fencr.tell()

def file_iterator(f, block_size, size):
    fencr.seek(0, 0)
    pos = 0
    while pos < size:
        rem = size-pos
        rs = min(rem, block_size)
        yield f.read(rs)
        pos += rs

print("[+] Decrypting file...")
# Decrypt
S = Salsa20.new(key=key, nonce=nonce)
for encrData in file_iterator(fencr, 2048, size-pos_key):
    data = S.decrypt(encrData)
    fdecr.write(data)

fdecr.close()
fencr.close()

print("[+] Decrypted file written to '%s'." % fdecrname)
