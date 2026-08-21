import time
from collections import defaultdict

class RateLimiter:
    """In-memory rate limiter using sliding window algorithm."""
    def __init__(self, max_requests: int = 5, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(list)

    def is_allowed(self, key: str) -> tuple:
        """Check if request is allowed for the given key (IP/username). Returns (allowed: bool, retry_after: int)."""
        now = time.time()
        # Clean older requests outside window
        window_start = now - self.window_seconds
        self.requests[key] = [t for t in self.requests[key] if t > window_start]
        
        if len(self.requests[key]) < self.max_requests:
            self.requests[key].append(now)
            return True, 0
        else:
            oldest_in_window = self.requests[key][0]
            retry_after = int(self.window_seconds - (now - oldest_in_window)) + 1
            return False, max(1, retry_after)

    def reset(self, key: str):
        """Reset rate limiter state for a given key."""
        if key in self.requests:
            del self.requests[key]
