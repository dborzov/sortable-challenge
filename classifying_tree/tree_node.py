import re, json
import matching

class UnrecognizedListing(Exception):
    pass

class NoMatchesForListing(UnrecognizedListing):
    pass

class AmbiguousMatchesForListing(UnrecognizedListing):
    pass

class BaseNode:
    """ Base class for classifying tree nodes """
    def __init__(self, label):
        self._children = []
        self.label = label
        self.product_counter = 0
        self.listing_counter = 0
        self.regexes = None
        self.parent = None

    def traverse(self, indent=""):
        """ prints the node's summary along with it's children """
        print
        print indent+ "{} [{} ps, {} ls]".format(self.label, self.product_counter, self.listing_counter)
        if self.regexes:
            print indent+ " (regex matchers: \"{}\")".format("\", \"".join(self.regexes))
        if len(self._children)==0:
            return
        print indent+ " --|"
        self._children = sorted(self._children, key=lambda x: -x.listing_counter)
        for child in self._children:
            child.traverse(indent="   | "+indent)
        print indent+ "   -"

    def write_result(self, fd):
        """
           recursively writes all the children's products with matched listings
           into fd file descriptor as jsonl
        """
        for child in self._children:
            child.write_result(fd)

    def search(self, listing):
        """ searches for matching products for a given listing """
        matches = []
        for child in self._children:
            if child.match(listing):
                matches.append(child)
        if len(matches)==0:
            raise NoMatchesForListing({
                "reason": "No matches",
                "decision_tree_node": self.label,
                "listing": listing
            })
        if len(matches)>1:
            raise AmbiguousMatchesForListing({
                "reason": "Several matches, should be excluding",
                "decision_tree_node": self.label,
                "matches": [m.label for m in matches],
                "listing": listing
            })
        return matches[0].search(listing)

    def check_4_collisions(self, product):
        for child in self._children:
            if child.match(product):
                return child
        return self

    def add_child(self, node):
        self._children.append(node)
        node.parent = self


class FamilyNode(BaseNode):
    """ Holds products with the same product family """
    def __init__(self, label, regexes):
        BaseNode.__init__(self, "Is family \"{}\"?".format(label))
        escaped_regexes = set([el.lower().rstrip() for el in regexes])
        self.regexes = escaped_regexes

    def match(self, listing):
        key = listing.get("title","").lower()
        for regex in self.regexes:
            if re.search(r'\b'+ regex + r'\b', key):
                return True
        return False

    def add_child(self, node):
        BaseNode.add_child(self, node)
        cur = node.parent
        while not cur is None:
            cur.product_counter += 1
            cur = cur.parent


class NoFamilyNode(FamilyNode):
    """ Products with empty family field go under this node"""
    def __init__(self):
        BaseNode.__init__(self, "Is family undefined?")

    def match(self, listing):
        return False


class ManufacturerNode(BaseNode):
    def __init__(self, label, regexes):
        BaseNode.__init__(self, "Is manufacturer \"{}\"?".format(label))
        escaped_regexes = set([el.lower().rstrip() for el in regexes])
        self.regexes = escaped_regexes
        self.undefined_family_node = NoFamilyNode()
        self.add_child(self.undefined_family_node)

    def traverse(self, indent=""):
        BaseNode.traverse(self,indent=indent)

    def match(self, listing):
        key = listing.get("manufacturer","").lower().rstrip()
        if not re.search("\w", key):
            key = listing.get("title","").lower()
        for regex in self.regexes:
            pattern = r'\b'+ regex + r'\b' if len(regex)<5 else regex
            if re.search(pattern, key):
                return True
        return False

    def search(self, listing):
        try:
            return BaseNode.search(self, listing)
        except NoMatchesForListing as e:
            if self.undefined_family_node.product_counter==0:
                raise e
            return self.undefined_family_node.search(listing)

    def assign_child(self, family_label):
        if not re.search("\w", family_label):
            return self.undefined_family_node
        tokens = matching.extract_tokens(family_label)
        variants = matching.generate_variants(tokens)
        regex = matching.tokens2regex(tokens)
        for v in variants:
            for child in self._children:
                if child.match({"title":v}):
                    child.regexes.add(regex)
                    return child
        new_node = FamilyNode(family_label, [regex])
        self.add_child(new_node)
        return new_node


class ModelNode(BaseNode):
    def __init__(self, result):
        self.label = result["model"]
        self.result = result
        self.regexes = [matching.label2regex(result["model"])]
        self.listings = []
        self.listing_counter = 0

    def match(self, listing):
        key = listing.get("title","").lower()
        for regex in self.regexes:
            if not re.search(r'\b'+ regex + r'\b', key):
                return False
        return True

    def write_result(self, fd):
        if len(self.listings)==0:
            return
        result = {
            "product_name": self.result["product_name"],
            "listings": self.listings
        }
        result_json = json.dumps(result)
        fd.write(result_json)
        fd.write("\n")

    def traverse(self, indent=""):
        print indent + self.label + "[{}]".format(len(self.listings))
        if self.regexes:
            print indent+ " (regex matchers: \"{}\")".format("\", \"".join(self.regexes))

    def search(self, listing):
        self.listings.append(listing)
        cur = self
        while True:
            cur.listing_counter += 1
            cur = cur.parent
            if cur is None:
                break
        return self

    def add_child(self):
        raise StandardError("Cant add children nodes to model node")

MANUFACTURER_SPECIAL_CASES = {
  "general electric": set([
    "general[\s-]*electric",
    "ge"
  ]),
  "fujifilm": set([
    "fuji[\s-]*film",
    "fuji"
  ]),
  "hp": set([
    "hp",
    "hewlett[\s-]*packard"
  ]),
  "konica minolta": set([
    "konica[\s-]*minolta",
    "konica",
    "minolta"
  ])
}

class Tree(BaseNode):
    def __init__(self):
        BaseNode.__init__(self,"root")
        for mf_name, mf_regexes in MANUFACTURER_SPECIAL_CASES.iteritems():
            mf_node = ManufacturerNode(mf_name, mf_regexes)
            self.add_child(mf_node)
