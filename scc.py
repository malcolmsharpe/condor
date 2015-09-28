from standings import *

racers = sorted(match_table)

fin = []
mark = set()

def dfs(v):
    if v in mark:
        return
    mark.add(v)

    for w in match_table[v]:
        if match_table[v][w] > 1:
            dfs(w)

    fin.append(v)

for r in racers:
    dfs(r)

mark.clear()

def revdfs(v):
    if v in mark:
        return
    mark.add(v)

    for w in match_table[v]:
        if match_table[w][v] > 1:
            revdfs(w)

    comp.add(v)

sccs = []

for r in reversed(fin):
    if r not in mark:
        comp = set()
        revdfs(r)
        sccs.append(comp)

sccs.sort(key=lambda x: len(x))

for comp in sccs:
    print 'Component; size = %d' % len(comp)
    names = sorted(comp)
    for r in names:
        print r
    print
