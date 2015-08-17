import re

inf_ms = 9999999

def ms_of_pb(pb):
    if pb == 'n/a':
        return inf_ms

    parts = re.split('[:.]', pb)
    assert len(parts) == 3
    return 10 * (int(parts[2]) + 100 * (int(parts[1]) + 60 * int(parts[0])))

def pb_of_ms(ms):
    ms //= 10

    cs = ms % 100
    ms //= 100
    s = ms % 60
    ms //= 60
    m = ms

    return '%02d:%02d.%02d' % (m, s, cs)
