from helpers import *

for l in listings:
    m = re.search(r'\w+',l.get("manufacturer",""))
    if m is None:
        print json.dumps(l)
