from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from handblog.config import Config
from flask_ckeditor import CKEditor


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
ckeditor = CKEditor()
mailed = Mail()

def create_app(config_class=Config):
    
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object(Config)
    login_manager.init_app(app) 
    mailed.init_app(app)
    db.init_app(app)
    ckeditor.init_app(app)

    from handblog.users.route import users
    from handblog.posts.route import posts
    from handblog.main.route import main
    from handblog.mail.route import mail
    from handblog.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(mail)
    app.register_blueprint(errors)

    with app.app_context():
        db.create_all()
        
    return app