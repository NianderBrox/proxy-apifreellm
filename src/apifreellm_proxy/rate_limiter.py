import asyncio
import time


class RateLimiter:

    def __init__(self, interval: float):
        self.interval = interval
        self._lock = asyncio.Lock()
        self._last_request = 0.0

    async def wait(self):

        async with self._lock:

            now = time.monotonic()

            elapsed = now - self._last_request

            if elapsed < self.interval:
                await asyncio.sleep(self.interval - elapsed)

            self._last_request = time.monotonic()