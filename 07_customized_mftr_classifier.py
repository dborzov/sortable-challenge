"""
Traverse through listings and see
if we can determine company for them and look in detail
at those for which we can't
"""

from helpers import *
import json, re

with open("sets/manufacturer_keys.txt","rb") as m_list:
    m_regexes = {l.rstrip(): l.rstrip() for l in m_list}

specials = json.loads(open("sets/company_classifier/special_cases.json","rb").read())
for key in specials.keys():
    for case in specials[key]:
        m_regexes[case] = key


stats = {
    "recognized": 0,
    "ambiguity": 0,
    "not recognized": 0,
    "total": 0,
}

for listing in JSONL("data/listings.txt"):
    key = listing["manufacturer"].lower()
    stats["total"] += 1
    matches = {}
    for regex, mftr in m_regexes.iteritems():
        mm = re.search(r'\b'+ regex + r'\b', key)
        if mm:
            matches[mftr] = True

    if len(matches.keys()) == 0:
        stats["not recognized"] += 1
    if len(matches.keys()) == 1:
        stats["recognized"] += 1
    if len(matches.keys()) > 1:
        print "AMBG| "+ key+ " |"+ ",".join(matches.keys())
        stats["ambiguity"] += 1

print stats
