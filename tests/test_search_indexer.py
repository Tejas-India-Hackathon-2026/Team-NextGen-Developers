import unittest
from modules.search_indexer import tokenize, MaterialSearchIndex

class TestSearchIndexer(unittest.TestCase):
    def test_tokenize(self):
        tokens = tokenize("Introduction to Data Structures and Algorithms!")
        self.assertIn("introduction", tokens)
        self.assertIn("data", tokens)
        self.assertIn("structures", tokens)
        self.assertIn("algorithms", tokens)
        self.assertNotIn("to", tokens)

    def test_search_index(self):
        idx = MaterialSearchIndex()
        idx.add_document("doc1", {
            "title": "Data Structures in C++",
            "subject": "DSA",
            "branch": "CSE",
            "semester": 3,
            "tags": ["trees", "graphs"],
            "description": "Comprehensive binary tree notes"
        })
        idx.add_document("doc2", {
            "title": "Digital Electronics Basics",
            "subject": "ECE",
            "branch": "ECE",
            "semester": 3,
            "tags": ["logic", "gates"],
            "description": "K-Maps and flip flops"
        })

        results = idx.search("binary trees")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "Data Structures in C++")

        filtered = idx.search("", branch="ECE")
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["subject"], "ECE")

if __name__ == "__main__":
    unittest.main()
