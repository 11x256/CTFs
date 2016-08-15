.NET APP just copy the validation code in 'btnCheck_Click' and bruteforce the 3 values, or you can analyze the code a bit more and find the xor deobfuscation. 

```
__author__ = 'abd el rahman'
#RGB.exe

x = [113,96,111,90,77,21,67,88,83,16,79,22,73,126,82,21,88,91,126,89,17,83,16,82,126,21,76,21,91,16,79,70,92]
key = x[3] ^ ord('{')
out =''
for i in x:
    out+=chr(key ^ i)
print out


print 'Brute forcing'
for value in range(0,256):
    for value2 in range(0,256):
        for value3 in range(0,256):
            num = value2 * value3;
            num2 = value * 3;
            if (value + num - value2 + value * value * value2 - value3 == value2 * (value3 * 34 + (num2 - value)) + 3744 and value > 60):
                print value,value2,value3
```
PAN{l4byr1n7h_s4yz_x0r1s_4m4z1ng}
