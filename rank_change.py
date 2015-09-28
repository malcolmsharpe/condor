import csv

def parse_ranks(path):
    rdr = csv.reader(file(path))

    rows = list(rdr)
    return rows

w8 = parse_ranks('out/bayeselo_week8.csv')
w9 = parse_ranks('out/bayeselo_week9.csv')

def rankmap(rows):
    ret = {}
    for row in rows[1:]:
        ret[row[1]] = int(row[0])
    return ret

w8r = rankmap(w8)
w9r = rankmap(w9)

wrt = csv.writer(file('out/bayeselo_week9_change.csv', 'wb'))

wrt.writerow(w9[0] + ['change'])

for row_old in w9[1:]:
    racer = row_old[1]

    rank_old = w8r[racer]
    rank_new = w9r[racer]

    change = rank_old - rank_new

    wrt.writerow(row_old + ['%+d' % change])
