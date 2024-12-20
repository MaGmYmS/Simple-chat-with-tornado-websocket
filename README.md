# Simple Chat Application

Это простое приложение чата, написанное на Python с использованием Tornado, WebSocket и Redis. Приложение позволяет пользователям обмениваться сообщениями в реальном времени и видеть список подключённых пользователей.

## Установка

1. Клонируйте репозиторий:
    ```sh
    git clone https://github.com/MaGmYmS/Simple-chat-with-tornado-websocket
    cd simple-chat
    ```

2. Создайте виртуальное окружение и активируйте его:
    ```sh
    python -m venv venv
    source venv/bin/activate  # Для Unix/MacOS
    .\venv\Scripts\activate  # Для Windows
    ```

3. Установите необходимые зависимости:
    ```sh
    pip install -r requirements.txt
    ```

4. Убедитесь, что у вас установлен и запущен Redis. Вы можете скачать и установить Redis с [официального сайта](https://redis.io/download), или вы можете создать контейнер в docker следующей командой.
   ```sh
   docker run --name redis -d -p 6379:6379 redis
   ```
## Запуск

Запустите приложение с помощью следующей команды:
   ```sh
   python server.py
   ```

Использование

   1) Откройте браузер и перейдите по адресу http://localhost:8080.
   2) Введите ваше имя в появившемся окне.
   3) Начните отправлять и получать сообщения в реальном времени.

Технологии

   1) Tornado: Асинхронный веб-фреймворк для Python.
   2) WebSocket: Протокол для обмена сообщениями в реальном времени.
   3) Redis: Хранилище данных в памяти, используемое для хранения истории сообщений и рассылки сообщений.
   4) HTML/CSS/JavaScript: Фронтенд часть приложения.
