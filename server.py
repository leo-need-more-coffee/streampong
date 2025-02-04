import os
import asyncio
from aiohttp import web
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

# Константы для клавиш
UP_KEY = [int(os.getenv("UP_KEY")), "UP"]
DOWN_KEY = [int(os.getenv("DOWN_KEY")), "DOWN"]

# Настройки игры
width = int(os.getenv("WIDTH", 40))
height = int(os.getenv("HEIGHT", 20))
ball_x = int(os.getenv("BALL_X", width // 2))
ball_y = int(os.getenv("BALL_Y", height // 2))
ball_dx = int(os.getenv("BALL_DX", 1))
ball_dy = int(os.getenv("BALL_DY", 1))
paddle_left = int(os.getenv("PADDLE_LEFT", height // 2))
paddle_right = int(os.getenv("PADDLE_RIGHT", height // 2))
paddle_height = int(os.getenv("PADDLE_HEIGHT", 4))
fps = int(os.getenv("FPS", 10))
frame_time = 1 / fps

PORT = os.getenv("PORT", 8000)
CLEAR_STRING = "\033[2J\033[H"


def draw_frame():
    frame = [[' ' for _ in range(width)] for _ in range(height)]

    # Рисуем мяч
    frame[ball_y][ball_x] = 'O'

    # Рисуем ракетки
    for i in range(paddle_height):
        if paddle_left + i < height:
            frame[paddle_left + i][0] = '|'
        if paddle_right + i < height:
            frame[paddle_right + i][width - 1] = '|'

    return '\n'.join(''.join(row) for row in frame)


def update_ball():
    global ball_x, ball_y, ball_dx, ball_dy, paddle_left, paddle_right

    # Обновляем позицию мяча
    ball_x += ball_dx
    ball_y += ball_dy

    # Проверка на столкновение с верхней и нижней границей
    if ball_y <= 0 or ball_y >= height - 1:
        ball_dy *= -1

    # Проверка на столкновение с ракетками
    if ball_x == 1 and paddle_left <= ball_y < paddle_left + paddle_height:
        ball_dx *= -1
    elif ball_x == width - 2 and paddle_right <= ball_y < paddle_right + paddle_height:
        ball_dx *= -1

    # Проверка на выход за границы
    if ball_x < 0 or ball_x >= width:
        ball_x = width // 2
        ball_y = height // 2


async def stream_frames(response):
    while True:
        update_ball()
        frame = draw_frame()

        # Отправляем кадр
        frame_data = frame.encode()
        frame_length = len(frame_data) + len(CLEAR_STRING)

        # Отправляем длину кадра в шестнадцатеричном формате
        await response.write(f"{frame_length:x}\r\n".encode())  # Длина кадра в шестнадцатеричном формате
        await response.write(CLEAR_STRING.encode())
        await response.write(frame_data + b'\r\n')  # Данные кадра

        await asyncio.sleep(frame_time)


async def healthcheck(request):
    return web.json_response({"status": "ok"})


async def handle_request(request):
    response = web.StreamResponse()
    response.content_type = 'text/plain'
    response.headers['Transfer-Encoding'] = 'chunked'
    await response.prepare(request)

    try:
        await stream_frames(response)
    except Exception as e:
        print(f"Connection closed: {e}")
    finally:
        await response.write_eof()

    return response


async def move_paddle_1(request):
    global paddle_left
    key = int(request.match_info['KEY'])

    if key == UP_KEY[0] and paddle_left > 0:
        paddle_left -= 1
    elif key == DOWN_KEY[0] and paddle_left < height - paddle_height:
        paddle_left += 1

    return web.json_response({"status": "ok", "paddle_left": paddle_left})


async def move_paddle_2(request):
    global paddle_right
    key = int(request.match_info['KEY'])

    if key == UP_KEY[0] and paddle_right > 0:
        paddle_right -= 1
    elif key == DOWN_KEY[0] and paddle_right < height - paddle_height:
        paddle_right += 1

    return web.json_response({"status": "ok", "paddle_right": paddle_right})


async def init_app():
    app = web.Application()
    app.router.add_get('/healthcheck', healthcheck)
    app.router.add_get('/', handle_request)
    app.router.add_get('/move/1/{KEY}', move_paddle_1)
    app.router.add_get('/move/2/{KEY}', move_paddle_2)
    return app


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(init_app())
    web.run_app(app, port=PORT)