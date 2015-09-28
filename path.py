import sys

from standings import *

racers = sorted(match_table)

s = sys.argv[1]
t = sys.argv[2]

assert s in racers
assert t in racers

prev = {s: None}

q = [s]

while q:
    q2 = []
    while q:
        v = q.pop()

        for w in match_table[v]:
            if match_table[v][w] > 0:
                if w not in prev:
                    prev[w] = v
                    q2.append(w)

    q = q2

if t not in prev:
    print 'No path found from %s to %s' % (s, t)
    sys.exit(1)

path = []
v = t

while True:
    path.append(v)
    if v == s:
        break
    v = prev[v]

path.reverse()
print 'Found path:'
for r in path:
    print r
print
print ' > '.join(path)
