import csv
import sys

matchup_path = 'data/CoNDOR Season 3 Matchup Chart - Week 1.csv'
pb_path = 'data/CoNDOR Season 3 Scouting - 8-2 PB Sorted.csv'
hype_path = 'out/week 1 hype.csv'

pb_map = {}
rdr = csv.reader(file(pb_path))
rows = list(rdr)
for row in rows[1:]:
    pb_map[row[0].lower()] = row[2]

recs = []

rdr = csv.reader(file(matchup_path))
for row in rdr:
    racer_1 = row[1]
    racer_2 = row[2]
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

wrt.writerow(['Max PB', 'Racer 1', 'Racer 2', 'Racer 1 PB', 'Racer 2 PB', 'Casted'])

recs.sort()
for max_pb, r1, r2, c in recs:
    pb1 = pb_map[r1.lower()]
    pb2 = pb_map[r2.lower()]
    wrt.writerow( (max_pb, r1, r2, pb1, pb2, c) )
