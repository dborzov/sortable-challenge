from helpers import *

products_by_p = collections.defaultdict(list)
for p in products:
    filepath = "sets/products_by_m/" + p["manufacturer"].rstrip().replace(" ","_").lower()
    products_by_p[filepath].append("{} ({})".format(p["model"],p.get("family","NONE")))

for each in products_by_p:
    with open(each,"w") as l:
        l.write("\n".join(sorted(products_by_p[each])))
