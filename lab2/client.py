import aiohttp
import asyncio
import json
from datetime import datetime


async def main():

    async with aiohttp.ClientSession() as session:
        request_data = json.dumps({'date': str(datetime.now())})
        async with session.post('http://0.0.0.0:8080/', data=request_data) as resp:
            print(resp.status)
            print(await resp.text())


loop = asyncio.get_event_loop()
loop.run_until_complete(main())