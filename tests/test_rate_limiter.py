import unittest
from modules.rate_limiter import RateLimiter

class TestRateLimiter(unittest.TestCase):
    def test_rate_limiter_allow_and_block(self):
        limiter = RateLimiter(max_requests=3, window_seconds=10)
        
        # First 3 requests allowed
        self.assertTrue(limiter.is_allowed("user_1")[0])
        self.assertTrue(limiter.is_allowed("user_1")[0])
        self.assertTrue(limiter.is_allowed("user_1")[0])
        
        # 4th request blocked
        allowed, retry_after = limiter.is_allowed("user_1")
        self.assertFalse(allowed)
        self.assertGreater(retry_after, 0)
        
        # Different user is unaffected
        self.assertTrue(limiter.is_allowed("user_2")[0])

    def test_reset(self):
        limiter = RateLimiter(max_requests=1, window_seconds=10)
        limiter.is_allowed("user_a")
        self.assertFalse(limiter.is_allowed("user_a")[0])
        
        limiter.reset("user_a")
        self.assertTrue(limiter.is_allowed("user_a")[0])

if __name__ == "__main__":
    unittest.main()
