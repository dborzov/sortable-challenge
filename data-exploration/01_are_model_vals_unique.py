"""
Are all the model fields unique?
"""

import helpers as h

unique_models = {}
for p in h.JSONL('data/products.txt'):
    if p["model"] in unique_models:
        print p["model"]
    unique_models["model"] = p["model"]

"""
Yes they are
"""
