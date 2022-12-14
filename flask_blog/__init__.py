from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_blog.config import Config
from flask_bcrypt import Bcrypt
from flask_mail import Mail

login_manager = LoginManager()
bcrypt = Bcrypt()
mail = Mail()
app = Flask(__name__)
db = SQLAlchemy(app)


def init_app():
    app.config.from_object(Config)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    db.init_app(app)
    mail.init_app(app)

    from flask_blog.main.routes import main
    from flask_blog.users.routes import users
    from flask_blog.posts.routes import posts
    from flask_blog.errors.handlers import errors

    app.register_blueprint(errors)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(users)
    return app
