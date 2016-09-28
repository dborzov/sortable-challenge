import unittest
import matching

class TestStringMatching(unittest.TestCase):
    def test_extract_tokens(self):
        test_pairs = [
            ("CyberShot", ["cyber", "shot"]),
            ("Cyber-Shot", ["cyber", "shot"]),
            ("Cyber_Shot", ["cyber", "shot"]),
            ("Cyber Shot", ["cyber", "shot"]),
            ("Cyber   Shot", ["cyber", "shot"]),
            ("C30", ["c", "30"]),
            ("C 30", ["c", "30"]),
            ("C-30", ["c", "30"]),
            ("PowerPC", ["power", "pc"])
        ]
        for in_label, expected in test_pairs:
            actual = matching.extract_tokens(in_label)
            self.assertEqual(expected, actual)
