import html
import re

def sanitize_text(text: str, max_length: int = 1000) -> str:
    """Sanitize user input string by stripping malicious HTML tags and trimming length."""
    if text is None:
        return ""
    # Strip HTML tags
    cleaned = re.sub(r'<[^>]*>', '', str(text))
    # Escape HTML special entities
    escaped = html.escape(cleaned)
    # Trim to maximum allowed length
    return escaped.strip()[:max_length]

def validate_email(email: str) -> bool:
    """Validate university email address format."""
    if not email or not isinstance(email, str):
        return False
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(pattern, email.strip()))

def sanitize_filename(filename: str) -> str:
    """Sanitize uploaded filename to prevent directory traversal and invalid characters."""
    if not filename:
        return "unnamed_document.pdf"
    # Remove path traversal tokens
    base = os_safe_basename = filename.replace("\\", "/").split("/")[-1]
    # Replace dangerous characters with underscore
    cleaned = re.sub(r'[^a-zA-Z0-9_.-]', '_', base)
    if not cleaned.lower().endswith(".pdf"):
        cleaned += ".pdf"
    return cleaned
