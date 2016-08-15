import struct
import base64
import string
def crypt(key,data,iv='\00\00\00\00\00\00\00\00',n=32):
    """
        Encrypt/decrypt variable length string using XTEA cypher as
        key generator (OFB mode)
        * key = 128 bit (16 char) 
        * iv = 64 bit (8 char)
        * data = string (any length)

        >>> import os
        >>> key = os.urandom(16)
        >>> iv = os.urandom(8)
        >>> data = os.urandom(10000)
        >>> z = crypt(key,data,iv)
        >>> crypt(key,z,iv) == data
        True

    """
    def keygen(key,iv,n):
        while True:
            iv = xtea_encrypt(key,iv,n)
            for k in iv:
                yield ord(k)
    xor = [ chr(x^y) for (x,y) in zip(map(ord,data),keygen(key,iv,n)) ]
    return "".join(xor)

def xtea_encrypt(key,block,n=32,endian="!"):
    """
        Encrypt 64 bit data block using XTEA block cypher
        * key = 128 bit (16 char) 
        * block = 64 bit (8 char)
        * n = rounds (default 32)
        * endian = byte order (see 'struct' doc - default big/network) 

        >>> z = xtea_encrypt('0123456789012345','ABCDEFGH')
        >>> z.encode('hex')
        'b67c01662ff6964a'

        Only need to change byte order if sending/receiving from 
        alternative endian implementation 

        >>> z = xtea_encrypt('0123456789012345','ABCDEFGH',endian="<")
        >>> z.encode('hex')
        'ea0c3d7c1c22557f'

    """
    v0,v1 = struct.unpack(endian+"2L",block)
    k = struct.unpack(endian+"4L",key)
    sum,delta,mask = 0L,0x9e3779b9L,0xffffffffL
    for round in range(n):
        v0 = (v0 + (((v1<<4 ^ v1>>5) + v1) ^ (sum + k[sum & 3]))) & mask
        sum = (sum + delta) & mask
        v1 = (v1 + (((v0<<4 ^ v0>>5) + v0) ^ (sum + k[sum>>11 & 3]))) & mask
    return struct.pack(endian+"2L",v0,v1)

def xtea_decrypt(key,block,n=32,endian="!"):
    """
        Decrypt 64 bit data block using XTEA block cypher
        * key = 128 bit (16 char) 
        * block = 64 bit (8 char)
        * n = rounds (default 32)
        * endian = byte order (see 'struct' doc - default big/network) 

        >>> z = 'b67c01662ff6964a'.decode('hex')
        >>> xtea_decrypt('0123456789012345',z)
        'ABCDEFGH'

        Only need to change byte order if sending/receiving from 
        alternative endian implementation 

        >>> z = 'ea0c3d7c1c22557f'.decode('hex')
        >>> xtea_decrypt('0123456789012345',z,endian="<")
        'ABCDEFGH'

    """
    v0,v1 = struct.unpack(endian+"2L",block)
    k = struct.unpack(endian+"4L",key)
    delta,mask = 0x9e3779b9L,0xffffffffL
    sum = (delta * n) & mask
    for round in range(n):
        v1 = (v1 - (((v0<<4 ^ v0>>5) + v0) ^ (sum + k[sum>>11 & 3]))) & mask
        sum = (sum - delta) & mask
        v0 = (v0 - (((v1<<4 ^ v1>>5) + v1) ^ (sum + k[sum & 3]))) & mask
    return struct.pack(endian+"2L",v0,v1)

key = 'AWildKeyAppears!'
s = 'B6XGLACYYUdwodupUtF0geaE5NKnf5gTiKxgwfWCJdi8Iq/b36ShdY/gs18m2VwpkTJPmg03FDpavvJF3EcAX8SUkrbpI1T61ZGKnrbD9gkf79eqi4giA4uKYEv9O/Iw3Godkhd0tB9e1ojQgW4307/OSTtWIzyEVhHbqkV694+fSZLD7FYMa80QYJQ5JRV/B6XGLACYYUdwodupUtF0geaE5NKnf5gT/Ycz/Ptt/q=='
s = s.translate(string.maketrans('qtgJYKa8y5L4flzMQ/BsGpSkHIjhVrm3NCAi9cbeXvuwDx+R6dO7ZPEno21T0UFW','ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'))

data =base64.b64decode(s)
out = ''
for i in range(0,len(data)-8 , 8):
    out+= xtea_decrypt(key , data[i:i+8],endian='@')
print out