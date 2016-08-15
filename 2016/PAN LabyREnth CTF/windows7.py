__author__ = 'abd el rahman'

wild = 'AWildKeyAppears!'


#PAN{did_1_mention_th0se_pupp3ts_fr34ked_m3_out_recent1y?}


for i in range(0,4):
    print hex(int(wild[i*4:(i*4)+4][::-1].encode('hex'),16))


def process_input(first,second):
    first = first
    first = int(first[::-1].encode('hex'),16)
    second = second
    second = int(second[::-1].encode('hex'),16)
    #h1= 0xBADA55
    h2= 0x9E3769B9
    #h3 = 0x4913092
    #h4 = 0x12345678
    #h5 = 0x0DEADBEEF
    var68 = 0
    counter = 0
    while counter < 0x20:
        eax = second
        eax <<= 4
        eax &=0xffffffff
        ecx = second
        ecx >>= 5
        eax = eax ^ ecx
        eax+=second
        eax &=0xffffffff
        edx = var68 & 3
        esi = var68 + int(wild[edx*4:(edx*4)+4][::-1].encode('hex'),16)
        esi &=0xffffffff
        eax ^=esi
        eax+=first
        eax &=0xffffffff
        first = eax
        # h1+=0xffc
        # var74 = 8
        # while var74 < 32:
        #     h4 <<= 3
        #     h4 &=0xffffffff
        #     h1-=40
        #     h3-=8
        #     var74+=1
        # h5=0x40
        eax = h2
        ecx = var68
        edx = ecx +0x1000 +eax
        var68 = edx
        var68 &= 0xffffffff
        eax = first
        eax <<=4
        eax &=0xffffffff
        ecx = first
        ecx >>=5
        eax^=ecx
        eax+=first
        eax &=0xffffffff
        edx = (var68 >> 11 ) & 3
        temp =  int(wild[edx*4:(edx*4)+4][::-1].encode('hex'),16)
        esi = var68 + temp
        esi &=0xffffffff
        eax = esi ^ eax
        second+=eax
        second&=0xffffffff
        counter +=1

    return (first),(second)

import string
for i in string.printable:
    print i
    for j in string.printable:
        for k in string.printable:
            for l in string.printable:
                if 0x2a140a4b ==  process_input('PAN{',i+j+k+l)[0]:
                    print i+j+k+l