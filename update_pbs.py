from bs4 import BeautifulSoup
import csv
import urllib2
import sys
import time

from pb_util import *

leaderboard_url = 'http://steamcommunity.com/stats/247080/leaderboards/740000/?xml=1'

#in_path = 'data/CoNDOR Season 3 Scouting - Copy of 8-2 Field.csv'
in_path = 'data/CoNDOR Season 3 Scouting - 8-23 PB Sorted.csv'
out_path = 'out/9-1 Field.csv'

f = urllib2.urlopen(leaderboard_url)
soup = BeautifulSoup(f)

pb_map = {}

for entry in soup.find_all('entry'):
    #<entry>
    #    <steamid>76561197998362244</steamid>
    #    <score>99698417</score>
    #    <rank>1</rank>
    #    <ugcid>700658678899103176</ugcid>
    #    <details>0400000006000000</details>
    #</entry>

    steamid = entry.find('steamid').text
    score = entry.find('score').text
    speed_ms = 100000000 - int(score)

    pb_map[steamid] = speed_ms

rdr = csv.reader(file(in_path))
rows = list(rdr)

wrt = csv.writer(file(out_path, 'wb'))
wrt.writerow( ['Name', 'toofz', 'PB', 'Change', 'Main Cast', 'Comments'] )

rows = rows[1:]
rows.sort(key=lambda row: row[2])

for row in rows:
    name, toofz, pb, old_change, main_cast, comments = row

    old_pb_ms = ms_of_pb(pb)

    steamid = unicode(toofz.split('/')[-1])
    pb_ms = pb_map[steamid]

    pb = pb_of_ms(pb_ms)

    change_ms = max(old_pb_ms - pb_ms, 0)
    if change_ms < 10:
        change = ''
    elif old_pb_ms == inf_ms:
        change = 'new'
    else:
        change = pb_of_ms(change_ms)

    print 'Writing: ', name, toofz, pb, change, main_cast, comments
    wrt.writerow( (name, toofz, pb, change, main_cast, comments) )
