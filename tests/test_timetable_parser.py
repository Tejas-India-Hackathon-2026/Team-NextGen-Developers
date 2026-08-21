import unittest
from modules.timetable_parser import find_schedule_conflicts, find_common_free_slots

class TestTimetableParser(unittest.TestCase):
    def test_find_schedule_conflicts(self):
        schedule = [
            {"day": "Monday", "start": "09:00", "end": "10:30", "subject": "DSA Lecture"},
            {"day": "Monday", "start": "10:00", "end": "11:00", "subject": "Maths Tutorial"},
            {"day": "Tuesday", "start": "09:00", "end": "10:00", "subject": "Physics"}
        ]
        conflicts = find_schedule_conflicts(schedule)
        self.assertEqual(len(conflicts), 1)
        self.assertEqual(conflicts[0]["day"], "Monday")

    def test_find_common_free_slots(self):
        user_schedules = {
            "alice": [{"day": "Wednesday", "start": "09:00", "end": "10:00"}],
            "bob": [{"day": "Wednesday", "start": "10:00", "end": "11:00"}]
        }
        all_slots = ["09:00-10:00", "10:00-11:00", "11:00-12:00", "12:00-13:00"]
        free = find_common_free_slots(user_schedules, "Wednesday", all_slots)
        self.assertIn("11:00-12:00", free)
        self.assertIn("12:00-13:00", free)
        self.assertNotIn("09:00-10:00", free)
        self.assertNotIn("10:00-11:00", free)

if __name__ == "__main__":
    unittest.main()
