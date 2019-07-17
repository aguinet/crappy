#!/usr/bin/env python3

import sys
import codecs
from Crypto.Cipher import ARC4
from tools import get_ransom_data

if len(sys.argv) < 2:
    print("Usage: %s ransom.txt" % sys.argv[0], file=sys.stderr)
    sys.exit(1)

data = get_ransom_data(sys.argv[1], "PC DATA")
decr = ARC4.new(b".oj=294~!z3)9n-1,8^)o((q22)lb$").decrypt(data)
print(codecs.decode(decr,"utf-16le"))
