__author__ = 'abd el rahman'


x = [ '\x16\x86\xF5\x96' , '\x56\x46\xF5\x37' , '\x76\x76\x57\x26' , '\x37\xF5\x27\x56' ,'\xC6\xC6\x96\xB6']

s = ''

for i in x :
    for j in i[::-1]:
        s+= chr(((ord(j) << 4 )& 255 )  | ((ord(j)>>4) & 255)   )
print s