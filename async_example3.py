import asyncio
import aiohttp
import random
import time


URL = "https://api.github.com/events"
MAX_CLIENTS = 10


async def aiohttp_get(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return response


async def fetch_async(pid):
    start = time.time()
    sleepy_time = random.randint(2, 5)
    print('Fetch async process {} started, sleeping for {} seconds'.format(
        pid, sleepy_time))
    response = await aiohttp_get(URL)
    datetime = response.headers.get('Date')

    response.close()
    return 'Process {}: {}, took: {:.2f} seconds'.format(
        pid, datetime, time.time() - start)


async def main():
    FUT = []
    start = time.time()
    futures = [fetch_async(i) for i in range(1, MAX_CLIENTS + 1)]
    for i, future in enumerate(asyncio.as_completed(futures)):
        result = await future
        if i % 2 == 0:
            FUT.append(result)
    return print(len(futures))


if __name__ == "__main__":
    asyncio.run(main())