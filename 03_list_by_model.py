"""
make a list of model vals only to see whether its easy to mix them up
or they are good ids
"""

import helpers as h

models = []
for p in h.JSONL('data/products.txt'):
    models.append((p["model"], p["manufacturer"], p.get("family")))

for m in sorted(models, key = lambda x:x[0]):
    print "{} ({}| {})".format(*m)
