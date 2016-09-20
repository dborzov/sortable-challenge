from solution import decision_tree, listings
import collections

listings_by_m = collections.defaultdict(list)
for l in listings:
    try:
        f = decision_tree.root.apply(l)
        filepath = "sets/listings_by_m/" + f + ".txt"
        listings_by_m[filepath].append(l["title"])
    except:
        continue

for each in listings_by_m:
    with open(each,"w") as l:
        l.write("\n".join([l.encode('utf-8') for l in sorted(listings_by_m[each])]))
