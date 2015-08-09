from bs4 import BeautifulSoup
import csv
import urllib2
import sys
import time

in_path = 'data/CoNDOR Season 3 Scouting - Copy of 8-2 Field.csv'
out_path = 'out/8-9 Field.csv'

REQ_DELAY = 5
def req_pb(toofz):
    print 'Waiting %d seconds before req' % REQ_DELAY
    time.sleep(REQ_DELAY)

    print 'Sending req'
    f = urllib2.urlopen(toofz)

    return parse_pb(f)

def parse_pb(f):
    # <tr data-character="Cadence" data-run="Speed" data-lbid="740000">
    #   <td>
    #     <a href="/leaderboards/cadence/speed?id=76561198067568785">Cadence</a>
    #   </td>
    #   <td> 66 </td>
    #   <td> 07:31.45 </td>
    # </tr>

    soup = BeautifulSoup(f, 'html.parser')
    el = soup.find(attrs={'data-character': 'Cadence', 'data-run': 'Speed'})
    pb = el.find_all('td')[-1].text.strip()
    if pb == '--':
        pb = 'n/a'

    return pb

rdr = csv.reader(file(in_path))
rows = list(rdr)

wrt = csv.writer(file(out_path, 'wb'))
wrt.writerow(rows[0])

for row in rows[1:]:
    name, toofz, pb, comments = row

    try:
        pb = req_pb(toofz)
    except Exception, e:
        print 'Req failed: ', e
        pb = 'failed'

    print 'Writing: ', name, toofz, pb, comments
    wrt.writerow( (name, toofz, pb, comments) )
