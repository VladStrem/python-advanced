import aiohttp
import aiohttp.web


# Обробник для GET-запиту
async def handle_get(request):
    name = request.rel_url.query.get('name', 'world')
    return aiohttp.web.Response(text=f"Hello, {name}!")
    # return aiohttp.web.Response(text="Це GET-запит")


# Обробник для POST-запиту
async def handle_post(request):
    data = await request.post()
    return aiohttp.web.Response(text=f"Це POST-запит з даними: {data}")


# Функція для створення веб-додатка
def create_app():
    app = aiohttp.web.Application()
    app.router.add_get('/get', handle_get)
    app.router.add_post('/post', handle_post)
    return app


# Запуск сервера
if __name__ == '__main__':
    app = create_app()
    aiohttp.web.run_app(app, host='127.0.0.1', port=8080)

# from aiohttp import web

# async def handle_hello(request):
#     name = request.rel_url.query.get('name', 'world')
#     return web.Response(text=f"Hello, {name}!")

# async def handle_echo(request):
#     data = await request.json()
#     return web.json_response(data)

# async def handle_status(request):
#     return web.Response(text="Server is running!")

# app = web.Application()
# app.router.add_get('/hello', handle_hello)  # Маршрут для обробки GET запиту /hello
# app.router.add_post('/echo', handle_echo)   # Маршрут для обробки POST запиту /echo
# app.router.add_get('/status', handle_status) # Маршрут для обробки статусу сервера

# if __name__ == '__main__':
#     web.run_app(app, port=8080)
