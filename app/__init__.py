from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_session import Session

db=SQLAlchemy() #database instance
bcrypt=Bcrypt() #password hashing instance
login_manager=LoginManager() #login manager instance
login_manager.login_view='users.login' #login view function name
login_manager.login_message="Please Log In to continue" #login message
login_manager.login_message_category="warning" #login message category
mail=Mail() #mail instance
db=SQLAlchemy() #database instance


from app.config import Config
def create_app(config_class=Config): 
    quiz_app=Flask(__name__)
    quiz_app.config.from_object(Config) #importing configurations from Config class
    
    db.init_app(quiz_app) #initializing database
    bcrypt.init_app(quiz_app) #initializing password hashing
    mail.init_app(quiz_app)  #initializing mail
    login_manager.init_app(quiz_app) #initializing login 
    Session(quiz_app)
    
    from app.main.routes import main
    quiz_app.register_blueprint(main) #registering users blueprint

    from app.users.routes import users
    quiz_app.register_blueprint(users) #registering users blueprint

    from app.quiz.routes import quiz
    quiz_app.register_blueprint(quiz) #registering quiz blueprint
    
    return quiz_app