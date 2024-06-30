from ratelimit import limits, sleep_and_retry
import threading

# Rate limit configuration: 100 requests per minute
REQUESTS = 100
MINUTES = 1

@sleep_and_retry
@limits(calls=REQUESTS, period=MINUTES * 60)
def limited_call():
    pass

class ConcurrencyControlMiddleware:
    def __init__(self):
        self.lock = threading.Lock()

    def __enter__(self):
        self.lock.acquire()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.lock.release()
