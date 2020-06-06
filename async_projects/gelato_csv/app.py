import aiohttp
import asyncio
import json
import os
import pandas
import time

from gelato_order import G_HEADERS, return_order, return_order_2 # dictionary format for a Gelato Request

DIRECTORY = os.listdir("csv_files")
GELATO_QUOTE = "https://api.gelato.com/v2/quote"

async def parse_employees():
    pass

async def parse_office(df):
    async with aiohttp.ClientSession(headers=G_HEADERS) as session:
        invocations = (parse_office_utility(row, session) for _, row in df.iterrows())
        invalid_csvs = await asyncio.gather(*invocations)
    # print(f"invalid_csvs: {invalid}")

async def parse_office_utility(row, session):
    country = row["Country"]
    office = row["Office Address"]
    city = row["City"]
    zip_code = row["Zip"]
    state = row["State"]
    # gelato_order = return_order_2()
    gelato_order = return_order(country, office, city, city, zip_code, state)
    response = await session.post(url=GELATO_QUOTE,
                                  json=gelato_order)
    
    print(response.__dict__)
    # print(response.code)
    value = await response.status
    value = json.loads(value)

async def iterate_over_files():
    for filename in DIRECTORY:
        if filename == "_offices.csv":
            values = await parse_office(pandas.read_csv(f"csv_files/{filename}"))
            print(values)

async def main():
    await iterate_over_files()

if __name__ == "__main__":
    print("main")
    start = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - start
    print(f"Executed in: {elapsed:0.2f} seconds")

    # iterate over the csv folder
    # if offices.csv --> make requests and figure out which offices are invalid.
    # if invalid --> put into invalid json, if valid (Do something)
    # iterate over employees.csv --> find out which employees belong to which office --> create invalid csv and valid csv
    # 