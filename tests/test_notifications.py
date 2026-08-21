import unittest
import os
import tempfile
from modules.notifications import send_notification, get_user_notifications, mark_as_read

class TestNotifications(unittest.TestCase):
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        self.temp_file.close()

    def tearDown(self):
        if os.path.exists(self.temp_file.name):
            os.remove(self.temp_file.name)

    def test_send_and_get_notifications(self):
        notif = send_notification("student_a", "Exam Alert", "Midsem dates released", db_path=self.temp_file.name)
        self.assertIsNotNone(notif.get("id"))
        self.assertEqual(notif["recipient"], "student_a")

        user_notifs = get_user_notifications("student_a", db_path=self.temp_file.name)
        self.assertEqual(len(user_notifs), 1)
        self.assertEqual(user_notifs[0]["title"], "Exam Alert")

    def test_mark_as_read(self):
        notif = send_notification("student_b", "Note Approved", "Your DSA notes were approved", db_path=self.temp_file.name)
        notif_id = notif["id"]

        unread = get_user_notifications("student_b", unread_only=True, db_path=self.temp_file.name)
        self.assertEqual(len(unread), 1)

        ok = mark_as_read(notif_id, db_path=self.temp_file.name)
        self.assertTrue(ok)

        unread_after = get_user_notifications("student_b", unread_only=True, db_path=self.temp_file.name)
        self.assertEqual(len(unread_after), 0)

if __name__ == "__main__":
    unittest.main()
