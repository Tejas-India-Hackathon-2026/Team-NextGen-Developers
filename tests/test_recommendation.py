import unittest
from modules.recommendation import recommend_materials

class TestRecommendation(unittest.TestCase):
    def setUp(self):
        self.materials = [
            {"id": "m1", "title": "CSE Algorithmic Design", "branch": "CSE", "semester": 4, "rating": 4.9, "downloads": 120},
            {"id": "m2", "title": "Civil Mechanics", "branch": "Civil", "semester": 4, "rating": 4.0, "downloads": 10},
            {"id": "m3", "title": "Universal Soft Skills", "branch": "Common", "semester": 4, "rating": 4.5, "downloads": 50},
        ]

    def test_recommendation_ranking(self):
        user = {"branch": "CSE", "semester": 4}
        recs = recommend_materials(user, self.materials, limit=2)
        self.assertEqual(len(recs), 2)
        # CSE specific should be top recommendation
        self.assertEqual(recs[0]["id"], "m1")

    def test_exclude_viewed(self):
        user = {"branch": "CSE", "semester": 4}
        recs = recommend_materials(user, self.materials, user_history=["m1"], limit=5)
        rec_ids = [r["id"] for r in recs]
        self.assertNotIn("m1", rec_ids)
        self.assertIn("m3", rec_ids)

if __name__ == "__main__":
    unittest.main()
