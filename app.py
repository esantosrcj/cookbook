
from flask import Flask

def create_app():
    app = Flask(__name__)

    app.config["JSON_SORT_KEYS"] = False

    from configs.settings import DATABASE_URL
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    # If set to True, Flask-SQLAlchemy will track modifications of objects and emit signals
    # This requires extar memory
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    from datetime import timedelta
    from configs.settings import SECRET_KEY
    # The secret key used to encode and decode JWTs when using a symmetric signing algorithm
    app.config["JWT_SECRET_KEY"] = SECRET_KEY
    # How long an access token should be valid before it expires
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    # How long an access token should be valid before it expires
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

    from extensions.db import db
    db.init_app(app)

    @app.before_first_request
    def create_tables():
        # This method will issue queries that first check for the existence of each individual table,
        # and if not found will issue the CREATE statements
        db.create_all()

    from extensions.api import api
    api.init_app(app)

    from extensions.jwt import jwt
    jwt.init_app(app)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()