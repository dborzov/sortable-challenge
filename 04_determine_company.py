"""
Traverse through listings and see
if we can determine company for them and look in detail
at those for which we can't
"""

from helpers import *

manufacturers = [l.rstrip() for l in open("sets/manufacturer_keys.txt")]
stats = {
    "recognized": 0,
    "ambiguity": 0,
    "not recognized": 0,
    "total": 0,
}

for listing in JSONL("data/listings.txt"):
    key = listing["manufacturer"].lower()
    stats["total"] += 1
    matches = 0
    for m in manufacturers:
        if m in key:
            matches += 1
    if matches == 0:
        stats["not recognized"] += 1
    if matches == 1:
        stats["recognized"] += 1
    if matches > 1:
        stats["ambiguity"] += 1

print stats
