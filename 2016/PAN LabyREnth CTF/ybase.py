__author__ = 'abd el rahman'
__author__ = 'abd el rahman'

s = 'B6XGLACYYUdwodupUtF0geaE5NKnf5gTiKxgwfWCJdi8Iq/b36ShdY/gs18m2VwpkTJPmg03FDpavvJF3EcAX8SUkrbpI1T61ZGKnrbD9gkf79eqi4giA4uKYEv9O/Iw3Godkhd0tB9e1ojQgW4307/OSTtWIzyEVhHbqkV694+fSZLD7FYMa80QYJQ5JRV/B6XGLACYYUdwodupUtF0geaE5NKnf5gT/Ycz/Ptt/q=='



import base64

import string

#s = 'djoBSg/M'
s = s.translate(string.maketrans('qtgJYKa8y5L4flzMQ/BsGpSkHIjhVrm3NCAi9cbeXvuwDx+R6dO7ZPEno21T0UFW','ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'))
print s
o = base64.b64decode(s)


o =list(o)

l = []
for i in range(0,len(o)-4,4):
    s = 0
    s+= (ord(o[i+3]) )
    s <<= 8
    s+= ord(o[i+2])
    s <<= 8
    s+= ord(o[i+1])
    s <<= 8
    s+= ord(o[i])
    l.append(hex(s))


for i in range(0,len(l)-1,2):
    print 'v[0] = ',l[i],';'
    print 'v[1] = ',l[i+1],';'
    print 'decipher(32,v,key);'