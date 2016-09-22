from io_helpers import *

class UnrecognizedListing(Exception):
    pass

class NoMatchesForListing(UnrecognizedListing):
    pass

class TreeNode:
    def __init__(self, label):
        self.children = []
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
        if len(self.children)==0:
            return
        print indent+ " --|"
        self.children = sorted(self.children, key=lambda x: -x.listing_counter)
        for child in self.children:
            child.traverse(indent="   | "+indent)
        print indent+ "   -"

    def write_result(self, fd):
        for child in self.children:
            child.write_result(fd)

    def search(self, listing):
        matches = []
        for child in self.children:
            if child.match(listing):
                matches.append(child)
        if len(matches)==0:
            raise NoMatchesForListing({
                "reason": "No matches",
                "decision_tree_node": self.label,
                "listing": listing
            })
        if len(matches)>1:
            raise UnrecognizedListing({
                "reason": "Several matches, should be excluding",
                "decision_tree_node": self.label,
                "matches": [m.label for m in matches],
                "listing": listing
            })
        return matches[0].search(listing)

    def apply_product(self, product):
        for child in self.children:
            if child.match(product):
                return child
        return self

    def add_child(self, node):
        self.children.append(node)
        node.parent = self

class FamilyNode(TreeNode):
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


class ManufacturerNode(TreeNode):
    def __init__(self, label, regexes):
        TreeNode.__init__(self, "Is manufacturer \"{}\"?".format(label))
        escaped_regexes = set([el.lower().rstrip() for el in regexes])
        self.regexes = escaped_regexes
        self.undefined_family_node = None

    def traverse(self, indent=""):
        TreeNode.traverse(self,indent=indent)
        if self.undefined_family_node:
            self.undefined_family_node.traverse(indent="   | "+indent)


    def match(self, listing):
        key = listing.get("manufacturer","").lower().rstrip()
        if not re.search("\w", key):
            key = listing.get("title","").lower()
        for regex in self.regexes:
            pattern = r'\b'+ regex + r'\b' if len(regex)<5 else regex
            if re.search(pattern, key):
                return True
        return False

    def undefined_family(self):
        if self.undefined_family_node:
            return self.undefined_family_node
        self.undefined_family_node = FamilyNode("Family NA", set())
        self.undefined_family_node.label = "Unspecified family products"
        self.undefined_family_node.parent = self
        return self.undefined_family_node

    def search(self, listing):
        try:
            return TreeNode.search(self, listing)
        except NoMatchesForListing as e:
            if not self.undefined_family_node:
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
        while(True):
            cur.listing_counter += 1
            cur = cur.parent
            if cur is None:
                break
        return self
