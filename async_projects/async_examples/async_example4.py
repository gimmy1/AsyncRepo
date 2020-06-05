import asyncio
import aiohttp
import time
from collections import namedtuple
from concurrent.futures import FIRST_COMPLETED


Service = namedtuple("Service", ("name", "url", "ip_attr"))

SERVICES = (
    Service('ipify', 'https://api.ipify.org?format=json', 'ip'),
    Service('ip-api', 'http://ip-api.com/json', 'query')
)

async def aiohttp_get(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.json()


async def fetch_ip(service):
    start = time.time()
    print(f"Fetching IP FROM {service.name}")

    json_response = await aiohttp_get(service.url)
    ip = json_response[service.ip_attr]

async def main():
    """ Illustrates how to send concurrent requests to an IP address. 
    First one that responds will be chosen!
    """
    futures = [fetch_ip(service) for service in SERVICES]
    # Schedule tasks with Wait
    # Retrieve results from the coroutine. Use done, pending. 
    done, pending = await asyncio.wait( 
        futures, return_when=FIRST_COMPLETED
    )
    print(done.pop().result())

if __name__ == "__main__":
    asyncio.run(main())