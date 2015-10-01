from collections import defaultdict
import csv
import random

from standings import *

dudes = list(totals)
dudes.sort(key=lambda x: totals[x])

print 'Top 9:'
for x in dudes[-9:]:
    print '  %s' % x
print

elig = []
for x in dudes[:-9]:
    if x not in dropped:
        elig.append(x)

points = defaultdict(lambda: 0)

pool = []
for x in elig:
    total = int(2*totals[x])
    points[total] += 1
    weight = total*total
    pool += [x] * weight

winners = []

while len(winners) < 4:
    x = random.choice(pool)
    if x not in winners:
        winners.append(x)

print 'Lotto winners (in order of selection):'
for x in winners:
    print '  (%2d) %s' % (totals[x], x)

wtr = csv.writer(file('lotto_ref.csv', 'wb'))

for x in sorted(points, reverse=True):
    wtr.writerow(['%.1f' % (x / 2.), points[x]])
