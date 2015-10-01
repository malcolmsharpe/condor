import collections
import csv
import re

from standings import *

pgn_path = 'out/condor_s3_final.pgn'

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
