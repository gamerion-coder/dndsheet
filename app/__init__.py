"""Flask app factory for dndsheet."""
from flask import Flask
from .db_config import init_db, close_connection

def create_app():
    app = Flask(
        __name__,
        template_folder='templates',
        static_folder='static'
    )
    app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'

    from . import routes
    routes.create_routes(app)
    app.register_blueprint(routes.api)

    init_db(app)
    app.teardown_appcontext(close_connection)

    return app