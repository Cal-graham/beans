from flask import Flask, render_template, session, request, redirect, url_for
from flask_session import Session
import siteFrame
import atexit


site_frame = siteFrame.SiteFrame()


def create_app():
    #   Create app instance
    app = Flask(__name__)
    Session(app);

    #   blueprint for all routes
    from main import main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/main')

    return app


if __name__ == "__main__":
    #   Run
    app = create_app()

    @app.route('/', methods=['GET', 'POST'])
    def index():
        return render_template('main.html')

    atexit.register(lambda: site_frame.exit())
    app.run(host='0.0.0.0', port=5000, debug=True)

