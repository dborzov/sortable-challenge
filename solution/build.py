"""
Parse the products dataset to
build DecisionTree
"""

from decision_tree import TreeNode, ManufacturerNode, FamilyNode, ModelNode, UnrecognizedListing
from io_helpers import *

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

decision_tree = TreeNode("root")

for mf_name, mf_regexes in MANUFACTURER_SPECIAL_CASES.iteritems():
    mf_node = ManufacturerNode(mf_name, mf_regexes)
    decision_tree.add_child(mf_node)

for p in products:
    # for given product, identify the manufacturer's node
    mf_label = p.get("manufacturer", "").lower().rstrip()
    if not mf_label:
        continue
    mf_node = decision_tree.apply_product({"manufacturer": mf_label})
    if mf_node.__class__ ==TreeNode:
        # if the manufacturer node does not exist, create one
        mf_node = ManufacturerNode(mf_label, [mf_label])
        decision_tree.add_child(mf_node)
    assert mf_node.__class__ == ManufacturerNode

    family_label = p.get("family", "").lower().rstrip()
    if family_label:
        family_node = mf_node.apply_product({"title": family_label})
        if family_node.__class__ == ManufacturerNode:
            new_family_node = FamilyNode(family_label, [family_label])
            mf_node.add_child(new_family_node)
            family_node= new_family_node
    else:
        family_node = mf_node.undefined_family()
    assert family_node.__class__ == FamilyNode

    model_label = p.get("model", "").lower().rstrip()
    if not model_label:
        continue
    model_node = ModelNode(p)
    family_node.add_child(model_node)
    for node in [decision_tree, mf_node, family_node]:
        node.product_counter += 1
