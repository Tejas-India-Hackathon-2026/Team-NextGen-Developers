import unittest
from modules.plagiarism_checker import calculate_cosine_similarity, check_duplicate_notes

class TestPlagiarismChecker(unittest.TestCase):
    def test_calculate_cosine_similarity_identical(self):
        text = "This is a detailed chapter on operating system scheduling algorithms and deadlocks."
        sim = calculate_cosine_similarity(text, text)
        self.assertAlmostEqual(sim, 100.0, places=1)

    def test_calculate_cosine_similarity_different(self):
        t1 = "Quantum physics thermodynamics fluid mechanics"
        t2 = "Python flask web frontend database design"
        sim = calculate_cosine_similarity(t1, t2)
        self.assertLess(sim, 10.0)

    def test_check_duplicate_notes(self):
        existing = [
            {"title": "Note A", "content_sample": "Binary search trees insertion and deletion algorithms"},
            {"title": "Note B", "content_sample": "Relational database normalization 1NF 2NF 3NF"}
        ]
        new_doc = "Binary search trees insertion and deletion algorithms with examples"
        res = check_duplicate_notes(new_doc, existing, threshold=80.0)
        self.assertTrue(res["is_duplicate"])
        self.assertEqual(res["matched_with"], "Note A")

if __name__ == "__main__":
    unittest.main()
