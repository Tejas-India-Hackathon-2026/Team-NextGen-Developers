import unittest
import os
import tempfile
from modules.audit_logger import log_event, query_logs

class TestAuditLogger(unittest.TestCase):
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        self.temp_file.close()

    def tearDown(self):
        if os.path.exists(self.temp_file.name):
            os.remove(self.temp_file.name)

    def test_log_event_creation(self):
        entry = log_event("USER_LOGIN", "student1", {"ip": "127.0.0.1"}, log_path=self.temp_file.name)
        self.assertEqual(entry["event_type"], "USER_LOGIN")
        self.assertEqual(entry["actor"], "student1")
        self.assertEqual(entry["status"], "SUCCESS")

    def test_query_logs_filter(self):
        log_event("LOGIN", "user1", {}, log_path=self.temp_file.name)
        log_event("UPLOAD", "user2", {}, log_path=self.temp_file.name)
        log_event("LOGIN", "user2", {}, log_path=self.temp_file.name)

        login_logs = query_logs(event_type="LOGIN", log_path=self.temp_file.name)
        self.assertEqual(len(login_logs), 2)

        user1_logs = query_logs(actor="user1", log_path=self.temp_file.name)
        self.assertEqual(len(user1_logs), 1)

if __name__ == "__main__":
    unittest.main()
