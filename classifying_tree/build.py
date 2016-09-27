"""
Functions that help building the tree
"""

from tree_node import Tree, BaseNode, ManufacturerNode, FamilyNode, ModelNode, UnrecognizedListing


def add_product(tree, product):
    """ add a product to the classifying tree """
    # for given product, identify the manufacturer's node
    mf_label = product.get("manufacturer", "").lower().rstrip()
    if not mf_label:
        return False
    mf_node = tree.check_4_collisions({"manufacturer": mf_label})
    if mf_node.__class__ ==Tree:
        # if the manufacturer node does not exist, create one
        mf_node = ManufacturerNode(mf_label, [mf_label])
        tree.add_child(mf_node)
    assert mf_node.__class__ == ManufacturerNode

    family_node = mf_node.assign_child(product.get("family", ""))
    assert issubclass(family_node.__class__, FamilyNode)

    model_label = product.get("model", "").lower().rstrip()
    if not model_label:
        return False
    model_node = family_node.check_4_collisions({"title": model_label})
    if not issubclass(model_node.__class__, FamilyNode):
        # there is already a matching model here, wont be creating duplicates
         return model_node
    model_node = ModelNode(product)
    family_node.add_child(model_node)
    return model_node
