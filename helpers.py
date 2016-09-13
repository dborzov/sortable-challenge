import json
import collections

class JSONL:
    def __init__(self, filepath):
        self.f = open(filepath, 'rb').__iter__()

    def __iter__(self):
        return self

    def next(self):
        line = self.f.next()
        return json.loads(line)


"""
count_values is a wrapper around value counter
"""
def count_values(path, getter):
    counter = collections.defaultdict(int)
    for item in JSONL(path):
        counter[getter(item)] += 1
    chart = sorted([(key, count) for key, count in counter.iteritems()], key=lambda x: -x[1])
    for val, count in chart:
        print "{}, {}".format(val, count)
