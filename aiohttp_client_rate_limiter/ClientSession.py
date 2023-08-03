import aiohttp
import asyncio
import logging

logger = logging.getLogger(__file__)


class RateLimitedClientSession(aiohttp.ClientSession):

    def __init__(self, max_concur, reqs_per_period, period_in_secs, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_concur = max_concur
        self.reqs_per_period = reqs_per_period
        self.period_in_secs = period_in_secs

        self.concur_semaphore = asyncio.Semaphore(max_concur)
        self.rete_limit_semaphore = asyncio.BoundedSemaphore(reqs_per_period)
        self.clock_on = True
        self.refiller = asyncio.create_task(self.token_refiller())

    async def token_refiller(self):

        while self.clock_on:
            time_for_next_req = self.period_in_secs/self.reqs_per_period
            logger.debug(f"Waiting {time_for_next_req} secs to allow next request...")
            # Wait for the time span that 1 new request could be fire
            await asyncio.sleep(time_for_next_req)

            # Add 1 more allowance only if current allowance are less then its max
            if self.rete_limit_semaphore._value < self.rete_limit_semaphore._bound_value:
                logger.debug(f"Allowing next request...")
                self.rete_limit_semaphore.release()

    async def _request(self, *args, **kwargs):

        # Making sure that there are only [self.max_concur] amount of request at the same time
        logger.debug(f"Getting Concurrency semaphore [{args}] ({self.concur_semaphore._value})...")
        await self.concur_semaphore.acquire()
        logger.debug(f"Concurrency semaphore acquired [{args}] ({self.concur_semaphore._value})...")

        # Making sure that this request will be made within the rate limited allowance
        logger.debug(f"Getting Rate limit semaphore [{args}] ({self.rete_limit_semaphore._value})...")
        await self.rete_limit_semaphore.acquire()
        logger.debug(f"Rate limit semaphore acquired [{args}] ({self.rete_limit_semaphore._value})...")

        resp = await super()._request(*args, **kwargs)
        logger.debug(f"--- Response received [{args}]...")

        # Release concurrent semaphore
        self.concur_semaphore.release()

        return resp

    async def close(self):
        logger.debug(f"Closing session...")
        self.clock_on = False
        await self.refiller
        logger.debug(f"Session closed...")
        await super().close()

