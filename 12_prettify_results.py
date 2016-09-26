from classifying_tree import JSONL
import json

products = {p["product_name"]:p for p in JSONL("data/products.txt")}
for i, result in enumerate(JSONL('results.jsonl')):
    with open("tmp/{}.jsonl".format(result["product_name"]),"w") as output:
        result["a_product"] = products[result["product_name"]]
        result["a_count"] = len(result["listings"])
        output.write(json.dumps(result, indent=4, sort_keys=True))
