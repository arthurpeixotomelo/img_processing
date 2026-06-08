import tempfile
import unittest
from pathlib import Path

from start_full_fast_analysis import parse_rgb_tuple, resolve_default_csv


class ParseRgbTupleTests(unittest.TestCase):
    def test_parses_numpy_like_tuple(self):
        value = "(np.int64(108), np.int64(104), np.int64(93))"
        self.assertEqual(parse_rgb_tuple(value), (108, 104, 93))

    def test_rejects_invalid_values(self):
        self.assertIsNone(parse_rgb_tuple("not-a-tuple"))
        self.assertIsNone(parse_rgb_tuple("(300, 1, 2)"))
        self.assertIsNone(parse_rgb_tuple(""))


class ResolveDefaultCsvTests(unittest.TestCase):
    def test_prefers_full_fast_filename(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            preferred = root / "image_analysis_results_full_fast.csv"
            fallback = root / "image_analysis_full.csv"
            preferred.write_text("x", encoding="utf-8")
            fallback.write_text("x", encoding="utf-8")

            self.assertEqual(resolve_default_csv(root), preferred)

    def test_uses_fallback_when_needed(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            fallback = root / "image_analysis_full.csv"
            fallback.write_text("x", encoding="utf-8")

            self.assertEqual(resolve_default_csv(root), fallback)

    def test_raises_when_missing(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with self.assertRaises(FileNotFoundError):
                resolve_default_csv(Path(tmpdir))


if __name__ == "__main__":
    unittest.main()
