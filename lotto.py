import random

from standings import *

dudes = list(totals)
dudes.sort(key=lambda x: totals[x])

print 'Top 9:'
for x in dudes[-9:]:
    print '  %s' % x
print
elig = dudes[:-9]

pool = []
for x in elig:
    total = int(2*totals[x])
    pool += [x] * (total*total)

winners = []

while len(winners) < 4:
    x = random.choice(pool)
    if x not in winners:
        winners.append(x)

print 'Lotto winners (in order of selection):'
for x in winners:
    print '  (%2d) %s' % (totals[x], x)
