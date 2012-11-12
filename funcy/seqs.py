from itertools import islice, ifilter, imap, izip, chain, tee, ifilterfalse


__all__ = ['count', 'repeat', 'repeatedly', 'iterate',
           'take', 'drop', 'first', 'rest',
           'imap', 'ifilter', 'remove', 'iremove', 'keep', 'ikeep',
           'concat', 'iconcat', 'cat', 'icat', 'mapcat', 'imapcat',
           'izip', 'interleave', 'interpose', 'distinct',
           'dropwhile', 'takewhile', 'isplit', 'split', 'groupby', 'chunks']


from itertools import count, repeat

def repeatedly(f, n=None):
    _repeat = repeat(None, n) if n else repeat(None)
    return (f() for _ in _repeat)

def iterate(f, x):
    while True:
        yield x
        x = f(x)


def take(n, coll):
    return list(islice(coll, n))

def drop(n, seq):
    return islice(seq, n, None)

def first(seq):
    return take(1, seq)

def rest(seq):
    return drop(1, seq)


# TODO: tree-seq equivalent

def remove(pred, coll):
    return filter(complement(pred), coll)

def iremove(pred, coll):
    return ifilter(complement(pred), coll)

def keep(f, seq):
    return filter(None, imap(f, seq))

def ikeep(f, seq):
    return ifilter(None, imap(f, seq))

def concat(*colls):
    return list(chain(*colls))
iconcat = chain

def cat(colls):
    return list(icat(colls))
icat = chain.from_iterable

def mapcat(f, *colls):
    return cat(imap(f, *colls))

def imapcat(f, *colls):
    return icat(imap(f, *colls))

def interleave(*seqs):
    return icat(izip(*seqs))

def interpose(sep, seq):
    return drop(1, interleave(repeat(sep), seq))


# Re-export
from itertools import dropwhile, takewhile

def distinct(seq):
    "Order preserving distinct"
    seen = set()
    return [x for x in seq if x not in seen and not seen.add(x)]

def isplit(at, seq):
    a, b = tee(seq)
    if callable(at):
        return ifilter(at, a), ifilterfalse(at, b)
    else:
        return islice(a, at), islice(b, at, None)

def split(at, seq):
    return map(list, isplit(at, seq))

# NOTE: should I name it cluster? to distinguish from itertools.groupby
def groupby(f, seq):
    result = defaultdict(list)
    for item in seq:
        result[f(item)].append(item)
    return result

def chunks(n, step, seq=None):
    if seq is None:
        return chunks(n, n, step)
    return [seq[i:i+n] for i in range(0, len(seq), step)]


def test_repeatedly():
    c = count().next
    assert take(2, repeatedly(c)) == [0, 1]