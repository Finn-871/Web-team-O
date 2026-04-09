from flask import Flask

def create_app():
    app = Flask(__name__)

    from .routes import events_bp
    app.register_blueprint(events_bp)

    return app
