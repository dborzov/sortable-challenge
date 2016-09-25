import unittest

class TestNoFamilyProduct(unittest.TestCase):
    """
     When a product json
     has no defined `family` field,
     it should go under the
     undefined_family_node
    """


    def setUp(self):
        from classifying_tree import Tree, add_product
        self.product = {
            "product_name":"Olympus_mju_9010",
            "manufacturer":"Olympus",
            "model":"mju 9010",
            "announced-date":"2010-01-06T19:00:00.000-05:00"
        }
        self.listing = {
            "currency": "CAD",
            "manufacturer": "Olympus",
            "price": "266.09",
            "title": "Olympus MJU 9010 12MP Digital Camera with 7x Dual Image Stabilized Zoom & 2.7\" LCD"
        }
        self.tree = Tree()
        self.product_node = add_product(self.tree, self.product)

    def test_product_node_position(self):
        import classifying_tree.tree_node
        self.assertIsInstance(
            self.product_node,
            classifying_tree.tree_node.ModelNode
        )
        self.assertIsInstance(
            self.product_node.parent,
            classifying_tree.tree_node.NoFamilyNode
        )
        self.assertIsInstance(
            self.product_node.parent.parent,
            classifying_tree.tree_node.ManufacturerNode
        )
        self.assertIsInstance(
            self.product_node.parent.parent.parent,
            classifying_tree.tree_node.BaseNode
        )
        self.assertIs(
            self.product_node.parent.parent.parent,
            self.tree
        )

    def test_tree_structure(self):
        self.assertEqual(len(self.product_node.parent._children), 1, msg="family level")
        self.assertEqual(len(self.product_node.parent.parent._children), 1, msg="mftr level")


    def test_product_counter(self):
        self.assertEqual(self.tree.product_counter, 1)

    def test_match(self):
        match = self.tree.search(self.listing)
        self.assertIs(match, self.product_node)
