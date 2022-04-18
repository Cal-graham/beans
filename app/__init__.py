from flask import Flask, render_template, session, request, redirect, url_for
from flask_session import Session
#from flask_sse import sse
#from quart import Quart, render_template, session, request, redirect, url_for

#from siteFrame import SiteFrame
#import atexit


def create_app():
    #   Create app instance
    app = Flask(__name__)
    #app.config["REDIS_URL"] = "redis://localhost"
    #app.register_blueprint(sse, url_prefix='/stream')
    #app = Quart(__name__)
    Session(app); #app.sf = SiteFrame()

    #   blueprint for all routes
    from main import main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/main')

    return app


if __name__ == "__main__":
    #   Run
    app_ = create_app();

    #@app_.route('/', methods=['GET', 'POST'])
    #def index():
    #    return render_template('main.html')

    app_.run(host='0.0.0.0', port=5000, debug=False)
