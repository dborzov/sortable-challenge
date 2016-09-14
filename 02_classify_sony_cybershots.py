"""
Looking into bielding a trie for subset
    manufacturer: Sony
    family: Cybershot
"""

import helpers as h

models = []
total_cnt = 0
for p in h.JSONL('data/products.txt'):
    if not p["manufacturer"]==u'Sony':
        continue
    if not p.get("family","").replace("-","").rstrip()=="Cybershot":
        continue
    total_cnt += 1
    models.append(p["model"])

assert total_cnt==42+6+8
models = sorted(models)
for m in models:
    print m
