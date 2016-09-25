import re

class UnrecognizedListing(Exception):
    pass

class NoMatchesForListing(UnrecognizedListing):
    pass

class AmbiguousMatchesForListing(UnrecognizedListing):
    pass

class TreeNode:
    """ Base class for tree nodes, also tree root node class """
    def __init__(self, label):
        self._children = []
        self.label = label
        self.product_counter = 0
        self.listing_counter = 0
        self.regexes = None
        self.parent = None

    def traverse(self, indent=""):
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
        for child in self._children:
            child.write_result(fd)

    def search(self, listing):
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

    def apply_product(self, product):
        for child in self._children:
            if child.match(product):
                return child
        return self

    def add_child(self, node):
        self._children.append(node)
        node.parent = self


class FamilyNode(TreeNode):
    """ Hold products with the same product family """
    def __init__(self, label, regexes):
        TreeNode.__init__(self, "Is family \"{}\"?".format(label))
        escaped_regexes = set([el.lower().rstrip() for el in regexes])
        self.regexes = escaped_regexes

    def match(self, listing):
        key = listing.get("title","").lower()
        for regex in self.regexes:
            if re.search(r'\b'+ regex + r'\b', key):
                return True
        return False

    def add_child(self, node):
        TreeNode.add_child(self, node)
        cur = node.parent
        while not cur is None:
            cur.product_counter += 1
            cur = cur.parent


class NoFamilyNode(FamilyNode):
    """ Products with empty family field go under this node"""
    def __init__(self):
        TreeNode.__init__(self, "Is family undefined?")

    def match(self, listing):
        return False

class ManufacturerNode(TreeNode):
    def __init__(self, label, regexes):
        TreeNode.__init__(self, "Is manufacturer \"{}\"?".format(label))
        escaped_regexes = set([el.lower().rstrip() for el in regexes])
        self.regexes = escaped_regexes
        self.undefined_family_node = NoFamilyNode()
        self.add_child(self.undefined_family_node)

    def traverse(self, indent=""):
        TreeNode.traverse(self,indent=indent)

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
            return TreeNode.search(self, listing)
        except NoMatchesForListing as e:
            if self.undefined_family_node.product_counter==0:
                raise e
            return self.undefined_family_node.search(listing)


class ModelNode(TreeNode):
    def __init__(self, result):
        self.label = result["model"]
        self.result = result
        self.regexes = []
        for token in self.result["model"].split():
                self.regexes.append(token.replace("-","[-\s]*"))
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
