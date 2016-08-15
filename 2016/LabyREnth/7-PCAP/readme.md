This challenge has two files , pcap file and exe file.
#PCAP file
There are only 2 ips communicating ,and one ip is always the sender.
Following the first TCP stream shows one char 'B', the second also shows one char '6'.  
So using scapy we can extract all these chars from the streams.
```
from scapy.all import *
f = rdpcap('p.pcap')

s = ''
for i in f:
	try:
		t = i.load
	except:
		continue
	s+=t
print s
```
This code will extract all the data sent.
```
B6XGLACYYUdwodupUtF0geaE5NKnf5gTiKxgwfWCJdi8Iq/b36ShdY/gs18m2VwpkTJPmg03FDpavvJF3EcAX8SUkrbpI1T61ZGKnrbD9gkf79eqi4giA4uKYEv9O/Iw3Godkhd0tB9e1ojQgW4307/OSTtWIzyEVhHbqkV694+fSZLD7FYMa80QYJQ5JRV/B6XGLACYYUdwodupUtF0geaE5NKnf5gT/Ycz/Ptt/q==
```
This looks like a base64 encoded string, the decoded output doesn't make any sense.
So let's start analyzing the exe file.

#EXE file

##Static analysis
The imports are not removed, networking functions are imported ![](1.PNG).  
Strings are not obfuscated and ,PEiD krypto analyzer didn't find any crypto signatures.ASLR is enabled for the exe.

##Dynamic / Code analysis

Cross referencing the send() function shows that it is called from a single function (sub_411D50), so this function must be responsible for sending the data.
Cross referencing this function shows that it is also called from a single function (sub_412300).
Function sub_411D50 pushes a string "file.txt" then calls sub_411316 ,which returns the address of a buffer sent to strlen(the buffer contains the data in "file.txt").

Then i created the file and started debugging. sub_411316 just returns the content of the file, so no need to analyze it for now .
sub_411AD0 requires that the input length is >= 8 then calls sub_411FF0.

The function at sub_411FF0 does some operations on the input .I didn't recognize it at first so i implemented this function in python, then i saw that 4 of the 5 hardcoded variables are not used ,after some searching for crypto constants i found that xtea algorithm uses 0x9E3779B9 ,and the fifth hardcoded value is 0x9E3769B9 ,and  0x1000 is added to it later , so this is the algorithm used to encrypt the data and the +0x1000 made PEiD miss it.

So we know have the key 'AWildKeyAppears!' sent as argument to sub_411FF0 and the data in the pcap file, but base64 decoding the data from the pcap file doesn't work.
so we need to know what happens after encrypting the data inf file.txt and before sending it.

sub_4111B3 is called with the cipher as argument, this function does base64 encoding but with a custom alphabet
```
qtgJYKa8y5L4flzMQ/BsGpSkHIjhVrm3NCAi9cbeXvuwDx+R6dO7ZPEno21T0UFW=
```
instead of the standard alphabet
```
ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=
```
base64 encoding simply takes 3 chars from the input - 2**8 possible value each- (3 * 8 bits) and produces 4 chars from the alphabet( 2**6 possible values each)  (4 * 6 bits).  


using the python implementation of xtea from https://en.wikipedia.org/wiki/XTEA i wrote a script to decrypt the data in the pcap file

```
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
```

PAN{did_1_mention_th0se_pupp3ts_fr34ked_m3_out_recent1y?}