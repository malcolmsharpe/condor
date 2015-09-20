import collections
import csv
import re

def ignore_opp(name):
    return ('withdrawn' in name
        or 'removed' in name
        or 'dropped' in name
        or name == ''
        or name == '(bye)'
        or name == '--')

def ignore_point(point):
    return (point.strip() == ''
        or '.' in point)

def canon(name):
    name = name.lower()

    if name == 'fakepsycho':
        return 'fakepsyho'
    if name == 'imwaytoopunny':
        return 'imwaytopunny'
    return name

decanon_map = {}

# forfeits, no-shows, intentional draws
noplays = set([
    # week 3
    ('ghost_butts', 'kageyuuki'),
    ('canadianbac0nz', 'ailoodee'),
    ('gfitty', 'zeldaethan9'),
    # week 4
    ('ghost_butts', 'violetweavile'),
    ('imwaytopunny', 'annierelli'),
    ('ognos', 'blueblimpsc'),
    ('flygluffet', 'morphobutterfly'),
    # week 5
    ('annierelli', 'ghost_butts'),
    ('jay__te', 'violetweavile'),
    # week 6
    ('miltrivd', 'paratroopa1'),
    ('morphobutterfly', 'ailoodee'),
    ('bmz_loop', 'emuemu7'),
    # week 7
    ('jay__te', 'ratata_ratata'),
])

def is_noplay(a, b):
    a = canon(a)
    b = canon(b)
    return (a,b) in noplays or (b,a) in noplays

standings_path = 'data/standings_week8.csv'
pgn_path = 'out/condor_s3_week8.pgn'

rdr = csv.reader(file(standings_path))
rows = list(rdr)

match_table = collections.defaultdict(lambda: {})

nweeks = 9

for row in rows:
    rank = row[0]
    racer = row[1]
    total = row[2]

    if not re.match('[0-9]+', rank):
        continue

    print 'Reading racer %s' % racer
    decanon_map[canon(racer)] = racer

    points = row[3:3+nweeks]
    opps = row[3+nweeks:3+2*nweeks]

    for point, opp in zip(points, opps):
        if ignore_opp(opp):
            print '    Ignoring opponent %r' % opp
            continue

        if ignore_point(point):
            print '    Ignoring point %r' % point
            continue

        if is_noplay(racer, opp):
            print '    Ignoring non-played match vs %r' % opp
            continue

        print '  %s from %s' % (point, opp)
        match_table[ canon(racer) ][ canon(opp) ] = int(point)
print

# Check consistency
for a in match_table:
    for b in match_table[a]:
        if b not in match_table:
            print 'Data inconsistency:'
            print '  %s is not the name of a racer' % b
        elif a not in match_table[b]:
            print 'Data inconsistency:'
            print '  %s did not play %s' % (b, a)
        elif match_table[a][b] + match_table[b][a] != 3:
            print 'Data inconsistency:'
            print '  %s got %d, %s got %d' % (match_table[a][b], match_table[b][a])
print

print 'Writing PGN'
f = file(pgn_path, 'w')

for a in sorted(match_table):
    for b in sorted(match_table[a]):
        for i in range(match_table[a][b]):
            print >>f, '[White "%s"]' % decanon_map[a]
            print >>f, '[Black "%s"]' % decanon_map[b]
            print >>f, '[Result "1-0"]'
            print >>f
            print >>f, '1-0'
            print >>f
