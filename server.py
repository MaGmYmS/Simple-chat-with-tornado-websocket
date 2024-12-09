import tornado.ioloop
import tornado.web
import tornado.websocket
import redis.asyncio as aioredis  # Используем асинхронный Redis клиент
import json
import asyncio
import logging

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)

# Асинхронный клиент Redis
redis_client = aioredis.Redis()

# Список имён подключённых клиентов
connected_clients = set()
user_names = {}  # Сопоставление WebSocket соединения и имени пользователя


class ChatWebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        # При подключении добавляем клиента в список
        connected_clients.add(self)
        user_names[self] = "Какой-то выскочка"
        self.broadcast_user_list()
        logging.debug(f"New client connected: {self}")

    async def on_message(self, message):
        try:
            # Проверяем, если это сообщение для смены имени
            data = json.loads(message)
            if "name" in data and "message" in data:
                user_names[self] = data["name"]  # Обновляем имя пользователя

                # Публикуем сообщение в Redis
                chat_message = json.dumps({"name": data["name"], "message": data["message"]})
                await redis_client.publish("chat_channel", chat_message)
                logging.debug(f"Received message from {data['name']}: {data['message']}")
            else:
                logging.error(f"Invalid message format: {message}")
        except json.JSONDecodeError:
            logging.error(f"Failed to decode JSON message: {message}")

    def on_close(self):
        # При отключении удаляем клиента из списка
        connected_clients.remove(self)
        user_names.pop(self, None)
        self.broadcast_user_list()
        logging.debug(f"Client disconnected: {self}")

    @staticmethod
    def broadcast_user_list():
        # Рассылка списка подключённых пользователей
        user_list = list(user_names.values())
        message = json.dumps({"type": "users", "users": user_list})
        for client in connected_clients:
            client.write_message(message)

    def check_origin(self, origin):
        return True


async def redis_listener():
    # Подписываемся на канал Redis
    pubsub = redis_client.pubsub()
    await pubsub.subscribe("chat_channel")

    # Обрабатываем входящие сообщения
    async for message in pubsub.listen():
        if message["type"] == "message":
            data = message["data"].decode("utf-8") if isinstance(message["data"], bytes) else message["data"]
            # Рассылаем сообщение всем подключённым клиентам
            for client in connected_clients:
                await client.write_message(data)
            logging.debug(f"Broadcasting message: {data}")


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        logging.debug("Serving index.html")
        self.render("static/index.html")


def create_app():
    return tornado.web.Application([
        (r"/", IndexHandler),
        (r"/chat", ChatWebSocketHandler),
        (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": "./static"}),
    ])


if __name__ == "__main__":
    app = create_app()
    app.listen(8080)
    print("Chat is available at http://localhost:8080")

    # Запуск Redis слушателя в асинхронном цикле
    loop = asyncio.get_event_loop()
    loop.create_task(redis_listener())

    # Запуск Tornado
    tornado.ioloop.IOLoop.current().start()
