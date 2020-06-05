import asyncio


async def foo():
    """ Declare coroutine """
    print("Running with foo")
    await asyncio.sleep(1) # mimic I/O time delay
    print("Running without foo")

async def bar():
    """ Declare coroutine """
    print("Running with bar")
    await asyncio.sleep(0) # mimic I/O time delay
    print("Running without bar")

async def main():
    """ Entrypoint coroutine """
    tasks = [foo(), bar()]
    await asyncio.gather(*tasks) # Unpack

if __name__ == "__main__":
    asyncio.run(main()) 

