
## Static analysis
Checking the file using PEiD or using CFF explorer shows that the file is packed using UPX.
I tried to unpack the file but it gave an error message saying that the file is hacked.
I saw this before in FLARE-ON challenge 2015 challlenge 4,it has a modified unpacking stub that if removed the output is changed.
So automatic unpacking will not work.
## Dynamic analysis
There are different ways to start debugging the packed executable,one way is to place a breakpoint at **popa** instruciton since the unpacking stub starts with **pusha** .
Then stepover functions calls a few time untill you see output in the console window, then the last function you stepped over was the function that is waiting for the input to be entered.
![](https://github.com/11x256/private-ctfs/blob/master/palo-alto/1-AntiD/1.PNG)  
*The addresses are different in every execution of the exe file*    
![](https://github.com/11x256/private-ctfs/blob/master/palo-alto/1-AntiD/2.PNG)
The function labeled "check_input" checks that the lengths of the input is 16 chars(input must be 16 chars), and it then takes 40 bytes from the input(input must be 40 chars) -This means that there is no valid input to the program- ,performs some operations and compare them to hardcoded values (40 local variables initialized at the start of the function).

This code reverses the operations done on the input and prints the flag.
```python
from ctypes import c_uint8
l = [0x8c,0xf1,0x53,0xa3,0x8,0xd7,0xdc,0x48,0xdb,0xc,0x3a,0xee,0x15,0x22,0xc4,0xe5,0xc9,0xa0,0xa5,0x0c,0xd3,0xdc,0x51,0xc7,0x39,0xfd,0xd0,0xf8,0x3b,0xe8,0xcc,0x3,0x6,0x43,0xf7,0xda,0x7e,0x65,0xae,0x80]
s=''
summ = 0 
for i in l:
    temp = i
    temp ^= summ
    temp += 0x66
    temp &= 0xff
    temp ^= 0x55
    temp = c_uint8(temp - 0x44).value
    temp ^= 0x33
    summ+=i
    s+= chr(temp)

print s
```

'check_input' functions calls some other functions to detect debugger, you can simply set register "al" to zero after each function call.

PAN{C0nf1agul4ti0ns_0n_4_J08_W3LL_D0N3!}