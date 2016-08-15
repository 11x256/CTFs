__author__ = 'abd el rahman'

class state():
    parent = ''
    table = ''
    move = ''

    def __init__(self, table=[], move='', parent=[]):
        self.table = table
        self.move = move
        self.parent = parent


f = 0
s = 0
r10 = 0
table = []  # first element is to keep the 1 based index
states = [[[0, 0, 13, 7]]]
history = [[state([0, 0, 13, 7], '', [])]]
c = -1
pairs = ['1 2', '1 3', '2 1', '2 3', '3 1', '3 2']
while (c < 15):
    c += 1
    history.append([])
    states.append([])
    for i in history[c]: # for every current state in history[c] , try to add each pair of input , if it results in a new state , add it in history[c+1]
        table = list(i.table)
        curr_table = list(i.table)
        for j in pairs:
            bad = 0
            f, s = map(int, j.split())
            if s == 1:
                r10 = 19
            elif s == 2:
                r10 = 13
            else:
                r10 = 7
            fv = table[f]
            sv = table[s]
            summ = fv + sv
            if summ <= r10:
                table[s] = summ
                table[f] = 0
            else:
                table[s] = r10
                table[f] = summ - r10
            if table == curr_table:
                continue  # state didn't change
            else:
                for k in history:  # state is changed
                    for kk in k:
                        if table == kk.table:
                            bad = 1 # state is a duplicate
                            break
                if bad == 0:
                    history[-1].append(state(list(table), str(j), i.table))

                table = list(curr_table)

target = ''
for i in history:
    for j in i:
        if j.table[1] == 10 and j.table[2] == 10:
            target = j

moves = []
while target.table != [0, 0, 13, 7]:
    moves.append(target.move)
    for i in history:
        for j in i:
            if j.table == target.parent:
                target = j
print 'Serial'
print ''.join(moves[::-1]).replace(' ', '')
