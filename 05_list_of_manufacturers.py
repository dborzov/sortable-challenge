import helpers as h
import collections

vals = collections.defaultdict(int)
for p in h.JSONL('data/products.txt'):
    vals[p.get("manufacturer", "none").lower().rstrip()] += 1

for e in sorted(vals.keys()):
    print e
