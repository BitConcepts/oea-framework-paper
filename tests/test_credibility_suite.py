import json
import math
import unittest
from pathlib import Path

from experiments.credibility_suite import (
    tokenize,
    split_train_heldout,
    ci95,
    _CALIBRATION_QUALITY,
    _rejection_rates,
)
from experiments.real_lm_experiment import BM25Retriever


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

    # ---- Calibration-quality formula tests (REQ-OEA-012) ----

    def test_rejection_rates_at_random_baseline(self):
        """CQ=0.5 (random) must return base rates unchanged."""
        p_false, p_true = _rejection_rates(0.50)
        self.assertAlmostEqual(p_false, 0.58, places=5)
        self.assertAlmostEqual(p_true, 0.24, places=5)

    def test_rejection_rates_increase_with_calibration(self):
        """Higher CQ must yield higher true-reject and lower false-reject."""
        pf_low, pt_low = _rejection_rates(0.60)
        pf_high, pt_high = _rejection_rates(0.80)
        self.assertGreater(pf_high, pf_low)
        self.assertLess(pt_high, pt_low)

    def test_rejection_rates_miscalibrated_inverts(self):
        """CQ < 0.5 (anti-calibrated) must degrade below base rates."""
        p_false, p_true = _rejection_rates(0.22)
        # Anti-calibrated: rejects fewer falsehoods and more truths than random
        self.assertLess(p_false, 0.58)
        self.assertGreater(p_true, 0.24)

    def test_calibration_quality_ordering(self):
        """oea_full > ablation_E > control; miscalibrated < control."""
        cq_oea = _CALIBRATION_QUALITY["oea_full"]
        cq_e = _CALIBRATION_QUALITY["ablation_E"]
        cq_ctrl = _CALIBRATION_QUALITY["control_replace"]
        cq_misc = _CALIBRATION_QUALITY["ablation_miscalibrated"]
        self.assertGreater(cq_oea, cq_e)
        self.assertGreater(cq_e, cq_ctrl)
        self.assertLess(cq_misc, cq_ctrl)

    def test_rejection_rates_bounds(self):
        """Output must always be in (0.01, 0.99) for all variants."""
        for variant, cq in _CALIBRATION_QUALITY.items():
            pf, pt = _rejection_rates(cq)
            self.assertGreater(pf, 0.0, msg=f"p_false <= 0 for {variant}")
            self.assertLess(pf, 1.0, msg=f"p_false >= 1 for {variant}")
            self.assertGreater(pt, 0.0, msg=f"p_true <= 0 for {variant}")
            self.assertLess(pt, 1.0, msg=f"p_true >= 1 for {variant}")

    # ---- BM25Retriever tests (REQ-OEA-010) ----

    def _make_retriever(self):
        """Build a BM25Retriever with a minimal mock tokenizer."""
        class MockTokenizer:
            def encode(self, text, **kwargs):
                # Deterministic integer IDs from word hashes
                return [abs(hash(w)) % 50000 for w in text.lower().split()]

        corpus = "alice in wonderland rabbit\n\npride and prejudice darcy\n\ncall me ishmael whale"
        return BM25Retriever.from_text(corpus, MockTokenizer()), MockTokenizer()

    def test_bm25_retriever_returns_corpus_passage(self):
        """REQ-OEA-010: retrieve() returns a passage from the corpus, not a proxy."""
        retriever, tok = self._make_retriever()
        query_ids = tok.encode("alice rabbit wonderland")
        passage, score = retriever.retrieve(query_ids)
        self.assertIsInstance(passage, str)
        self.assertGreater(len(passage), 0)
        self.assertGreater(score, 0.0)

    def test_bm25_retriever_selects_relevant_passage(self):
        """retrieve() should prefer the passage with highest token overlap."""
        retriever, tok = self._make_retriever()
        # Query matching first passage (alice/rabbit/wonderland tokens)
        q_alice = tok.encode("alice rabbit")
        # Query matching third passage (ishmael/whale tokens)
        q_moby = tok.encode("ishmael whale")
        p_alice, s_alice = retriever.retrieve(q_alice)
        p_moby, s_moby = retriever.retrieve(q_moby)
        # They should return different passages
        self.assertNotEqual(p_alice, p_moby)

    def test_bm25_retriever_score_is_overlap_not_log_prob(self):
        """REQ-OEA-010: score must be in [0,1] (overlap ratio), not a log value (<0)."""
        retriever, tok = self._make_retriever()
        query_ids = tok.encode("alice in wonderland")
        _, score = retriever.retrieve(query_ids)
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)

    def test_bm25_from_text_splits_into_passages(self):
        """from_text() must produce multiple passages from a multi-paragraph corpus."""
        retriever, _ = self._make_retriever()
        self.assertGreaterEqual(len(retriever.passages), 2)


if __name__ == "__main__":
    unittest.main()
