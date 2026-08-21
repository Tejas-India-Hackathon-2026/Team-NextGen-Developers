import unittest
from modules.gamification import calculate_tier, evaluate_badges, build_leaderboard

class TestGamification(unittest.TestCase):
    def test_calculate_tier(self):
        self.assertEqual(calculate_tier(0)["name"], "Novice Scholar")
        self.assertEqual(calculate_tier(60)["name"], "Apprentice Scholar")
        self.assertEqual(calculate_tier(350)["name"], "Distinguished Fellow")
        self.assertEqual(calculate_tier(800)["name"], "Academic Grandmaster")

    def test_evaluate_badges(self):
        profile = {"karma": 150}
        badges = evaluate_badges(profile, upload_count=6, avg_rating=4.8)
        self.assertIn("FIRST_UPLOAD", badges)
        self.assertIn("PROLIFIC_AUTHOR", badges)
        self.assertIn("KARMA_CENTURION", badges)
        self.assertIn("TOP_RATED", badges)
        self.assertNotIn("CAMPUS_LEGEND", badges)

    def test_build_leaderboard(self):
        users_db = {
            "alice": {"name": "Alice", "karma": 120, "role": "student", "badges": ["b1"]},
            "bob": {"name": "Bob", "karma": 250, "role": "student", "badges": []},
            "prof_smith": {"name": "Prof Smith", "karma": 999, "role": "faculty"}
        }
        board = build_leaderboard(users_db)
        self.assertEqual(len(board), 2)
        self.assertEqual(board[0]["username"], "bob")
        self.assertEqual(board[0]["rank"], 1)
        self.assertEqual(board[1]["username"], "alice")
        self.assertEqual(board[1]["rank"], 2)

if __name__ == "__main__":
    unittest.main()
