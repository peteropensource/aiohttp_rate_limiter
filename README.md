# aiohttp_client_rate_limiter

This is a mini tool that overwrites ClientSession class from aiohttp (https://pypi.org/project/aiohttp/). This subclass could provide rate limter function while sending out requests within same session.

Example:
```python
import asyncio
from aiohttp_client_rate_limiter.ClientSession import RateLimitedClientSession

client_session = RateLimitedClientSession(
        max_concur=5,
        reqs_per_period=10,
        period_in_secs=60
    )
tasks = [asyncio.create_task(client_session.get(f"https://www.google.com/?q={i}", ssl=False)) for i in range(10)]

await asyncio.gather(*tasks)

await client_session.close()
```
The above example could provide a steady rate of 10 requests/60 seconds at the maximum concurrency of 5.