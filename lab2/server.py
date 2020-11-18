from aiohttp import web
import json


routes = web.RouteTableDef()


@routes.post('/')
async def handle(request):
    print(request.text)
    await request.text()
    if not request.body_exists:
        error = json.dumps({'error': 'you should enter your date of birth'})
        return web.Response(text=error, status=400)
    else:
        return web.Response(text=await request.text(), status=200)

if __name__ == '__main__':
    app = web.Application()
    app.router.add_routes(routes)
    web.run_app(app)
