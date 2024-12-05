from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
bcrypt = Bcrypt()
csrf = CSRFProtect()
migrate = Migrate()

login_manager = LoginManager()
login_manager.login_view = 'main.login'

def creat_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate = Migrate(app, db)
    bcrypt.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app,db)

    login_manager.init_app(app)
    
    with app.app_context():
        from .routes import main
        app.register_blueprint(main)
        
        db.create_all()
        
    return app
