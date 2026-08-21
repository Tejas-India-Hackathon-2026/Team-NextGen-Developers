import unittest
from modules.quiz_engine import evaluate_quiz_submission, get_sample_flashcards

class TestQuizEngine(unittest.TestCase):
    def setUp(self):
        self.questions = [
            {"id": "q1", "question": "2+2?", "options": ["3", "4", "5"], "correct_option_index": 1, "explanation": "Math basics"},
            {"id": "q2", "question": "Capital of France?", "options": ["Berlin", "Madrid", "Paris"], "correct_option_index": 2, "explanation": "Geography"}
        ]
        self.flashcards = [
            {"id": "f1", "subject": "DSA", "term": "Array", "definition": "Contiguous memory"},
            {"id": "f2", "subject": "DSA", "term": "Stack", "definition": "LIFO"},
            {"id": "f3", "subject": "OS", "term": "Process", "definition": "Program in execution"}
        ]

    def test_evaluate_perfect_quiz(self):
        answers = {"q1": 1, "q2": 2}
        result = evaluate_quiz_submission(self.questions, answers)
        self.assertEqual(result["score"], 2)
        self.assertEqual(result["total"], 2)
        self.assertEqual(result["percentage"], 100.0)
        self.assertTrue(result["passed"])

    def test_evaluate_partial_quiz(self):
        answers = {"q1": 1, "q2": 0}
        result = evaluate_quiz_submission(self.questions, answers)
        self.assertEqual(result["score"], 1)
        self.assertEqual(result["percentage"], 50.0)
        self.assertFalse(result["passed"])

    def test_get_sample_flashcards(self):
        cards = get_sample_flashcards(self.flashcards, count=2, subject="DSA")
        self.assertEqual(len(cards), 2)
        for c in cards:
            self.assertEqual(c["subject"], "DSA")

if __name__ == "__main__":
    unittest.main()
