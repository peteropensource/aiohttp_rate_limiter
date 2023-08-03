# aiohttp_client_rate_limiter

This is a mini tool that overwrites ClientSession class from aiohttp (https://pypi.org/project/aiohttp/). This subclass introduces rate limter functionality while leaving all the other parent behaviors untouched.

Example:
```python
import asyncio
from aiohttp_client_rate_limiter.ClientSession import RateLimitedClientSession

rl_session = RateLimitedClientSession(
        max_concur=5,
        reqs_per_period=10,
        period_in_secs=60
    )
tasks = [asyncio.create_task(rl_session.get(f"https://www.google.com/?q={i}", ssl=False)) for i in range(10)]

await asyncio.gather(*tasks)

await rl_session.close()
```

Or, we could simply do this, using the native context manager as provided by aiohttp:
```python
import asyncio
from aiohttp_client_rate_limiter.ClientSession import RateLimitedClientSession

async with RateLimitedClientSession(
    max_concur=60,
    reqs_per_period=5,
    period_in_secs=10
) as rl_session:
    tasks = [asyncio.create_task(rl_session.get(f"https://www.google.com/?q={i}", ssl=False)) for i in range(10)]
    await asyncio.gather(*tasks)
```
The above example could provide a steady rate of 10 requests/60 seconds at the maximum concurrency of 5.