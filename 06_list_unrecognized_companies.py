from helpers import *
import collections

manufacturers = [l.rstrip() for l in open("sets/manufacturer_keys.txt")]
unknown_manufacturers = collections.defaultdict(int)

for listing in JSONL("data/listings.txt"):
    key = listing["manufacturer"].lower()
    matches = 0
    for m in manufacturers:
        if m in key:
            matches += 1
    if matches == 0:
        unknown_manufacturers[key] += 1

with open("sets/company_classifier/unrecognized.txt", "wb") as dd:
    for e in sorted([(key, val) for key, val in unknown_manufacturers.iteritems()], key=lambda x:-x[1]):
        dd.write(e[0].encode('utf-8') + ":" + str(e[1])+"\n")
