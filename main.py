from flask import Flask, jsonify
import threading
import time

from Scan import Game

app = Flask(__name__)


# Функция для фонового выполнения
def background_task():
    game = Game()
    while True:
        game.move()
        time.sleep(0.4)


background_task()
'''if __name__ == '__main__':
    # Запуск фоновой задачи в отдельном потоке
    background_thread = threading.Thread(target=background_task)
    background_thread.daemon = True  # Позволяет завершить поток при остановке программы
    background_thread.start()

    # Запуск Flask-сервера
    app.run(host='0.0.0.0', port=5000)'''
