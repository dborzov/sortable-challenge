import unittest
import matching

class TestStringMatching(unittest.TestCase):
    def test_extract_tokens(self):
        test_pairs = [
            ("CyberShot", ["cyber", "shot"]),
            ("PowerPC", ["power", "pc"])
        ]
        for in_label, expected in test_pairs:
            actual = matching.extract_tokens(in_label)
            self.assertEqual(expected, actual)
