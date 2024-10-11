import os

from flask import Flask
import config


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
