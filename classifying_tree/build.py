"""
Parse the products dataset to
build DecisionTree
"""

from tree_node import TreeNode, ManufacturerNode, FamilyNode, ModelNode, UnrecognizedListing

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

tree = TreeNode("root")

for mf_name, mf_regexes in MANUFACTURER_SPECIAL_CASES.iteritems():
    mf_node = ManufacturerNode(mf_name, mf_regexes)
    tree.add_child(mf_node)

def add_product(tree, product):
    # for given product, identify the manufacturer's node
    mf_label = product.get("manufacturer", "").lower().rstrip()
    if not mf_label:
        return False
    mf_node = tree.apply_product({"manufacturer": mf_label})
    if mf_node.__class__ ==TreeNode:
        # if the manufacturer node does not exist, create one
        mf_node = ManufacturerNode(mf_label, [mf_label])
        tree.add_child(mf_node)
    assert mf_node.__class__ == ManufacturerNode

    family_label = product.get("family", "").lower().rstrip()
    if family_label:
        family_node = mf_node.apply_product({"title": family_label})
        if family_node.__class__ == ManufacturerNode:
            new_family_node = FamilyNode(family_label, [family_label])
            mf_node.add_child(new_family_node)
            family_node= new_family_node
    else:
        family_node = mf_node.undefined_family_node
    assert issubclass(family_node.__class__, FamilyNode)

    model_label = product.get("model", "").lower().rstrip()
    if not model_label:
        return False
    model_node = family_node.apply_product({"title": model_label})
    if not issubclass(model_node.__class__, FamilyNode):
        # there is already a matching model here, wont be creating duplicates
         return model_node
    model_node = ModelNode(product)
    family_node.add_child(model_node)
    return model_node
