import aiohttp
import asyncio
import json
from datetime import datetime


async def main():

    async with aiohttp.ClientSession() as session:
        # request_data = json.dumps({'month': 11, 'day': 15})
        print("Please input your birth date and month")
        birth_date = dict()
        birth_date["day"] = input("day: ")
        birth_date["month"] = input("month: ")
        request_data = json.dumps(birth_date)

        async with session.post('http://0.0.0.0:8080/', data=request_data) as resp:
            print("status code: ", resp.status)
            print(json.loads(await resp.text())["result"])


loop = asyncio.get_event_loop()
loop.run_until_complete(main())