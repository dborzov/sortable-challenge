import unittest, re
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

    def test_tokens2regex_matching(self):
        regex = matching.tokens2regex(["cyber", "shot"])
        matching_variants = [
            "cybershot",
            "cyber shot",
            "cyber   shot",
            "cyber-shot",
            "cyber-_-shot"
        ]

        for v in matching_variants:
            m = re.search(r'\b'+ regex + r'\b', v)
            self.assertIsNotNone(m)


    def test_tokens2regex_nonmatching(self):
        regex = matching.tokens2regex(["cyber", "shot"])
        non_matching_variants = [
            "cybershotty",
            "cyber elizabeth shot",
            "megacyber-shot",
            "shot cyber"
        ]
        for v in non_matching_variants:
            m = re.search(r'\b'+ regex + r'\b', v)
            self.assertIsNone(m, msg=v)
