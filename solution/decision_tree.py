from io_helpers import *

class UnRecognizedListing(Exception):
    pass

class DecisionTree:
    def __init__(self, matcher_func, label=""):
        self.matcher = matcher_func
        self.children = []
        self.label = label
        self.result = None

    def match(self, listing):
        return self.matcher(listing)

    def traverse(self, indent=""):
        string = indent+ "{}".format(self.label)
        if len(self.children)==0:
            print string
            return
        print string +  " ->"
        for child in self.children:
            child.traverse(indent="   "+indent)


    def apply(self, listing):
        if self.result:
            return self.result
        matches = []
        for child in self.children:
            if child.match(listing):
                matches.append(child)
        if len(matches)==0:
            raise UnRecognizedListing({
                "reason": "No matches",
                "decision_tree_node": self.label,
                "listing": listing
            })
        if len(matches)>1:
            raise UnRecognizedListing({
                "reason": "Several matches, should be excluding",
                "decision_tree_node": self.label,
                "matches": [m.label for m in matches],
                "listing": listing
            })
        return matches[0].apply(listing)

root = DecisionTree(lambda x: True, label="Decision Tree Root")

# regexes for manufacturers
manufacturers = collections.defaultdict(set)
for p in products:
    mf = p.get("manufacturer","").lower().rstrip()
    if mf == "":
        continue
    manufacturers[mf].add(mf)

for case in manufacturer_special_cases:
    if not case in manufacturers:
        continue
    for regex in manufacturer_special_cases[case]:
        manufacturers[case].add(regex)



def factory_manufacturer_matcher(name, regexes):
    def mf_matcher(listing):
        key = listing.get("manufacturer","").lower()
        for regex in regexes:
            if re.search(r'\b'+ regex + r'\b', key):
                return True
        return False
    return mf_matcher

# manufacturer filter level
for mf, regexes in manufacturers.iteritems():
    matcher = factory_manufacturer_matcher(mf, regexes)
    label = "is manufacturer \"{}\"?".format(mf)
    node = DecisionTree(matcher, label=label)
    node.result = mf
    root.children.append(node)
