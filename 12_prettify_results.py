from classifying_tree import JSONL
import json

products = {p["product_name"]:p for p in JSONL("data/products.txt")}
for i, result in enumerate(JSONL('results.jsonl')):
    with open("tmp/"+str(i)+".jsonl","w") as output:
        result["a_product"] = products[result["product_name"]]
        output.write(json.dumps(result, indent=4, sort_keys=True))
