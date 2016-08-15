__author__ = 'abd el rahman'
import random
f = 0
s = 0
r10 = 0
table = [0,0,13,7]
history = []
pairs = ['1 2' , '1 3', '2 1' , '2 3', '3 1' ,'3 2']
while(table[1] !=10 or table[2] !=10):
    f,s = map(int,raw_input().split())
    #f,s = map(int,pairs[random.randint(0,len(pairs)-1)].split())
    if table == [0,0,13,7]:
        history = []
    if f == s :
        print ' f == s '
        continue
    if s == 1 :
       r10 = 19
    elif s == 2 :
        r10=13
    else:
        r10 = 7
    fv = table[f]
    sv = table[s]
    summ = fv + sv
    if summ <= r10:
        table[s] = summ
        table[f]=0
    else:
        table[s]=r10
        table[f]=summ-r10
    history.append(str(f)+str(s))
    print table

print 'founddd'
print history