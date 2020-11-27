from aiohttp import web
import json
from aiopg.sa import create_engine

from sqlalchemy.sql import text
from populate_db import forecast
from datetime import datetime


routes = web.RouteTableDef()


async def _calculate_value(month, day):
    return ((month * 2 + day) % 9) + 1


@routes.post('/')
async def handle(request):
    print(request.text)
    request_body = json.loads(await request.text())
    print(request_body)
    if not request_body:
        error = json.dumps({'error': 'you should enter your date of birth'})
        return web.Response(text=error, status=400)
    else:
        id = await _calculate_value(int(request_body['month']), int(request_body['day']))
        async with create_engine(user='student',
                                 database='mmhpc',
                                 host='127.0.0.1',
                                 password='passwd') as engine:
            async with engine.acquire() as conn:
                queryset = await conn.execute(forecast.select(whereclause=text(f'id={id}')))
                result = await queryset.first()
                if not result:
                    return web.Response(text="Failed calling the database", status=200)
                response_text = json.dumps({'result': result[1]})
        return web.Response(text=response_text, status=200)

if __name__ == '__main__':
    app = web.Application()
    app.router.add_routes(routes)
    web.run_app(app)
