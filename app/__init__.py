from flask import Flask, render_template, session, request, redirect, url_for
from flask_session import Session
import atexit


def create_app():
    #   Create app instance
    app = Flask(__name__)
    Session(app)

    #   blueprint for all routes
    from main import main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/main')

    return app


if __name__ == "__main__":
    #   Run
    app_ = create_app()

    @app_.route('/', methods=['GET', 'POST'])
    def index():
        return render_template('main.html')

    app_.run(host='0.0.0.0', port=5000, debug=True)
