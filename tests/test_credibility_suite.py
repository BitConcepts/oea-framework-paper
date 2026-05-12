import json
import unittest
from pathlib import Path

from experiments.credibility_suite import tokenize, split_train_heldout, ci95


class TestCredibilitySuite(unittest.TestCase):
    def test_tokenize_basic(self):
        toks = tokenize("Hello, world! It's 2026.")
        self.assertIn("hello", toks)
        self.assertIn("world", toks)
        self.assertIn("it's", toks)
        self.assertIn("2026", toks)

    def test_split_train_heldout(self):
        tokens = [str(i) for i in range(100)]
        train, heldout = split_train_heldout(tokens, heldout_frac=0.2)
        self.assertEqual(len(train), 80)
        self.assertEqual(len(heldout), 20)

    def test_ci95_monotonic(self):
        m, lo, hi = ci95([1, 2, 3, 4, 5])
        self.assertLessEqual(lo, m)
        self.assertLessEqual(m, hi)


if __name__ == "__main__":
    unittest.main()
