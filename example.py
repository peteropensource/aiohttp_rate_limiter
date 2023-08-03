import logging
import asyncio
from aiohttp_client_rate_limiter.ClientSession import RateLimitedClientSession


async def main():

    rl_session = RateLimitedClientSession(
        max_concur=60,
        reqs_per_period=5,
        period_in_secs=10
    )
    tasks = [asyncio.create_task(rl_session.get(f"https://www.google.com/?q={i}", ssl=False)) for i in range(10)]

    await asyncio.gather(*tasks)

    await rl_session.close()


async def main2():

    async with RateLimitedClientSession(
        max_concur=60,
        reqs_per_period=5,
        period_in_secs=10
    ) as rl_session:
        tasks = [asyncio.create_task(rl_session.get(f"https://www.google.com/?q={i}", ssl=False)) for i in range(10)]
        await asyncio.gather(*tasks)


if __name__ == "__main__":

    # This following method is only used to config the root logger so that debug message would be print to console
    def config_root_logger():
        root_logger = logging.getLogger()
        root_logger.setLevel('DEBUG')

        console_handler = logging.StreamHandler()
        console_handler.setLevel('DEBUG')

        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        console_handler.setFormatter(formatter)

        root_logger.addHandler(console_handler)

    config_root_logger()

    asyncio.run(main())
    asyncio.run(main2())

