"""
Defines Tree, the root node of the tree
(and a reference to the whole tree, as a result)
"""

from tree_node import BaseNode, ManufacturerNode
from special_cases import MANUFACTURER_SPECIAL_CASES

class Tree(BaseNode):
    def __init__(self):
        BaseNode.__init__(self,"root")
        for mf_name, mf_regexes in MANUFACTURER_SPECIAL_CASES.iteritems():
            mf_node = ManufacturerNode(mf_name, mf_regexes)
            self.add_child(mf_node)
