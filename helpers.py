import json, re
import collections

class JSONL:
    def __init__(self, filepath):
        self.f = open(filepath, 'rb').__iter__()

    def __iter__(self):
        return self

    def next(self):
        line = self.f.next()
        return json.loads(line)


listings = JSONL('data/listings.txt')
products = JSONL('data/products.txt')

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


class MnftrClassifier:
    def __init__(self):
        with open("sets/manufacturer_keys.txt","rb") as m_list:
            self.m_regexes = {l.rstrip(): l.rstrip() for l in m_list}

        specials = json.loads(open("sets/company_classifier/special_cases.json","rb").read())
        for key in specials.keys():
            for case in specials[key]:
                self.m_regexes[case] = key

    def classify(self,listing):
        key = listing.get("manufacturer","").lower()
        matches = {}
        for regex, mftr in self.m_regexes.iteritems():
            mm = re.search(r'\b'+ regex + r'\b', key)
            if mm:
                matches[mftr] = True

        if len(matches.keys()) == 0:
            return None
        if len(matches.keys()) == 1:
            return matches.keys()[0]
        if len(matches.keys()) > 1:
            return None

mnft_classifier = MnftrClassifier()
