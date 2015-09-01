import csv
import sys

from common import *
from pb_util import *

matchup_path = 'data/CoNDOR Season 3 Matchup Chart - Week 4.csv'
pb_path = 'data/CoNDOR Season 3 Scouting - 8-23 PB Sorted.csv'
hype_path = 'out/week 4 hype.csv'

pb_map = {}
rdr = csv.reader(file(pb_path))
rows = list(rdr)
for row in rows[1:]:
    pb_map[row[0].lower()] = row[2]

recs = []

rdr = csv.reader(file(matchup_path))
for row in rdr:
    racer_1 = retouch_racer(row[1])
    racer_2 = retouch_racer(row[2])
    casted = row[3]

    pb_1 = pb_map.get(racer_1.lower())
    pb_2 = pb_map.get(racer_2.lower())

    if not pb_1:
        print 'No PB for %s' % racer_1
    if not pb_2:
        print 'No PB for %s' % racer_2

    if pb_1 and pb_2:
        recs.append( (max(pb_1, pb_2), racer_1, racer_2, casted) )


wrt = csv.writer(file(hype_path, 'wb'))

wrt.writerow(['Max PB', 'Diff PB', 'Racer 1', 'Racer 2', 'Racer 1 PB', 'Racer 2 PB', 'Casted'])

recs.sort()
for max_pb_old, r1, r2, c in recs:
    pb1 = pb_map[r1.lower()]
    pb2 = pb_map[r2.lower()]

    ms1 = ms_of_pb(pb1)
    ms2 = ms_of_pb(pb2)

    max_ms = max(ms1, ms2)
    diff_ms = abs(ms1 - ms2)

    max_pb = 'n/a'
    diff_pb = 'n/a'
    if ms1 != inf_ms and ms2 != inf_ms:
        max_pb = pb_of_ms(max_ms)
        diff_pb = pb_of_ms(diff_ms)

    wrt.writerow( (max_pb, diff_pb, r1, r2, pb1, pb2, c) )
