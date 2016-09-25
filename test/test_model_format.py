import unittest

class TestModelFormat(unittest.TestCase):
    """
     When a product json
     has no defined `family` field,
     it should go under the
     undefined_family_node
    """
    def setUp(self):
        from classifying_tree import Tree, add_product
        self.product = {
            "product_name":"HP_Photosmart_C30",
            "manufacturer":"HP",
            "model":"C30",
            "family":"Photosmart",
            "announced-date":"1998-10-25T19:00:00.000-05:00"
        }

        self.listing = {
            "title":"HP PhotoSmart C30 - Digital camera - compact - 1.0 Mpix - supported memory: CF",
            "manufacturer":"Hewlett Packard",
            "currency":"USD",
            "price":"19.99"
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
            classifying_tree.tree_node.FamilyNode
        )
        self.assertIsInstance(
            self.product_node.parent.parent,
            classifying_tree.tree_node.ManufacturerNode
        )
        self.assertIsInstance(
            self.product_node.parent.parent.parent,
            classifying_tree.tree_node.Tree
        )
        self.assertIs(
            self.product_node.parent.parent.parent,
            self.tree
        )

    def test_tree_structure(self):
        self.assertEqual(len(self.product_node.parent._children), 1, msg="family level")
        self.assertEqual(len(self.product_node.parent.parent._children), 2, msg="mftr level")


    def test_product_counter(self):
        self.assertEqual(self.tree.product_counter, 1)

    def test_match(self):
        # import pdb; pdb.set_trace()
        match = self.tree.search(self.listing)
        self.assertIs(match, self.product_node)
