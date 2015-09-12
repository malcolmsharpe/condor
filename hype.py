import csv
import sys

from common import *
from pb_util import *

matchup_path = 'data/CoNDOR Season 3 Matchup Chart - Week 6.csv'
pb_path = 'data/CoNDOR Season 3 Scouting - Sep 8 PB Sorted.csv'
hype_path = 'out/week 6 hype.csv'
los_path = 'out/los.csv'

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

    pb_1 = pb_map.get(racer_1.lower())
    pb_2 = pb_map.get(racer_2.lower())

    if not pb_1:
        print 'No PB for %s' % racer_1
    if not pb_2:
        print 'No PB for %s' % racer_2

    if pb_1 and pb_2:
        recs.append( (max(pb_1, pb_2), racer_1, racer_2) )

# read LOS
def name_to_los(name):
    if name == 'MacKirbyTwitch':
        return 'MacKirby'
    if name == 'Lancer':
        return 'Lancer873'
    return name

los = {}

rdr = csv.reader(file(los_path))
rows = list(rdr)

los_order = [row[0] for row in rows[1:]]

for row in rows[1:]:
    a = row[0]
    los[a] = {}

    for b, p in zip(los_order, row[1:]):
        if len(p) < 2:
            p = (2 - len(p)) * '0' + p
        los[a][b] = p

wrt = csv.writer(file(hype_path, 'wb'))

wrt.writerow(['Max PB', 'Diff PB', 'Racer 1', 'Racer 2', 'Racer 1 PB', 'Racer 2 PB', 'Elo Favorite', 'LOS'])

recs.sort()
for max_pb_old, r1, r2 in recs:
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

    r1_los = name_to_los(r1)
    r2_los = name_to_los(r2)

    a_los = los[r1_los][r2_los]
    b_los = los[r2_los][r1_los]

    if a_los > b_los:
        fav = r1
        fav_los = a_los
    else:
        fav = r2
        fav_los = b_los

    wrt.writerow( (max_pb, diff_pb, r1, r2, pb1, pb2, fav, fav_los) )
