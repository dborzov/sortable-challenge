class UnRecognizedListing(Exception):
    pass

class DecisionTree:
    def __init__(self, matcher_func, label=""):
        def.matcher = matcher_func
        self.children = []
        self.label = label
        self.match = None

    def match(self, listing):
        return self.matcher(listing)

    def apply(self, listing):
        matches = []
        if self.match:
            return self.match
        for child in children:
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
                "matches": [m.label for m in matches]
                "listing": listing
            })
        matches[0].apply(listing)
