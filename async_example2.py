import asyncio
import aiohttp
import time


URL = 'https://api.github.com/events'
MAX_CLIENTS = 10

async def aiohttp_get(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return response

async def fetch_async(pid):
    response = await aiohttp_get(URL)
    datetime = response.headers.get('Date')

    response.close()
    return datetime

async def main():
    tasks = [
        asyncio.create_task(
            fetch_async(i)) for i in range(1, 10)
    ]
    await asyncio.wait(tasks)

if __name__ == "__main__":
    asyncio.run(main())