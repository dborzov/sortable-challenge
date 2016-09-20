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
# manufacturers is a dict with keys a manufacturer id/names
# and values a set of regexes
manufacturers = collections.defaultdict(set)
mf_families = collections.defaultdict(set)
for p in products:
    mf = p.get("manufacturer","").lower().rstrip()
    if mf == "":
        continue
    manufacturers[mf].add(mf)
    family = p.get("family","").lower().rstrip()
    if family=="":
        continue
    mf_families[mf].add(family)
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

def factory_family_matcher(name, regexes):
    def family_matcher(listing):
        key = listing.get("title","").lower()
        for regex in regexes:
            if re.search(r'\b'+ regex + r'\b', key):
                return True
        return False
    return mf_matcher

# manufacturer filter level
for mf, regexes in manufacturers.iteritems():
    mf_matcher = factory_manufacturer_matcher(mf, regexes)
    label = "is manufacturer \"{}\"?".format(mf)
    node = DecisionTree(mf_matcher, label=label)
    root.children.append(node)
    for family in mf_families[mf]:
        f_matcher = factory_family_matcher(family, [family])
        label = "is family \"{}\"?".format(family)
        fm_node = DecisionTree(f_matcher, label=label)
        fm_node.result = "mf: {}, f: {}".format(mf, family)
        node.children.append(fm_node)
    if len(mf_families[mf])==0:
        node.result = mf
