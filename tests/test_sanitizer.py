import unittest
from modules.sanitizer import sanitize_text, validate_email, sanitize_filename

class TestSanitizer(unittest.TestCase):
    def test_sanitize_text_strips_tags(self):
        dirty = "<script>alert('pwned')</script>Hello <b>World</b>"
        clean = sanitize_text(dirty)
        self.assertNotIn("<script>", clean)
        self.assertNotIn("<b>", clean)
        self.assertIn("Hello", clean)
        self.assertIn("World", clean)

    def test_validate_email(self):
        self.assertTrue(validate_email("student@university.edu.in"))
        self.assertTrue(validate_email("john.doe@college.ac.in"))
        self.assertFalse(validate_email("invalid_email_format"))
        self.assertFalse(validate_email("user@.com"))

    def test_sanitize_filename(self):
        bad_name = "../../etc/passwd/notes#1?.pdf"
        clean_name = sanitize_filename(bad_name)
        self.assertNotIn("..", clean_name)
        self.assertNotIn("/", clean_name)
        self.assertTrue(clean_name.endswith(".pdf"))

if __name__ == "__main__":
    unittest.main()
