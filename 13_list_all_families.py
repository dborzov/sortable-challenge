from classifying_tree import JSONL
import json

a = set()
for p in JSONL("data/products.txt"):
    a.add(p.get("family","NONE"))

family_names = sorted([e for e in a])
with open("sets/families.txt","w") as output:
    for family_name in family_names:
            output.write(family_name+"\n")
