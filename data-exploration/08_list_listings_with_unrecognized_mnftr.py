from helpers import *

chart = collections.defaultdict(int)
for l in listings:
    if mnft_classifier.classify(l) is None:
        chart[l["manufacturer"]] += 1
ordered = sorted([(key,count) for key, count in chart.iteritems()], key=lambda x:-x[1])
for key, val in ordered:
    print "{}|{}".format(key.encode('utf-8'),val)
