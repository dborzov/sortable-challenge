import unittest
from classifying_tree import Tree, add_product

class TestMatchingSeparators(unittest.TestCase):
    """
     When a product json
     has no defined `family` field,
     it should go under the
     undefined_family_node
    """
    def setUp(self):
        self.product_a = {
            "announced-date": "2000-02-01T19:00:00.000-05:00",
            "family": "Cyber-shot",
            "manufacturer": "Sony",
            "model": "DSC-S70",
            "product_name": "Sony_Cyber-shot_DSC-S70"
        }

        self.product_b = {
            "announced-date": "2000-02-01T19:00:00.000-05:00",
            "family": "CyberShot",
            "manufacturer": "Sony",
            "model": "DSC-S70",
            "product_name": "Sony_Cyber-shot_DSC-S70"
        }


    def test_match_dashed_with_camelcase(self):
        tree = Tree()
        node_a = add_product(tree, self.product_a)
        node_b = add_product(tree, self.product_b)
        self.assertIs(node_a, node_b)


    def test_match_camelcase_with_dashed(self):
        tree = Tree()
        node_b = add_product(tree, self.product_b)
        node_a = add_product(tree, self.product_a)
        self.assertIs(node_a, node_b)
