from app import db, login_manager
from flask_login import UserMixin, current_user
from flask import current_app

class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),unique=True,nullable=False)
    email=db.Column(db.String(),unique=True, nullable=False)
    pro_img=db.Column(db.String(),nullable=False,default='default.png')
    password=db.Column(db.String(10),nullable=False)
    max_score=db.Column(db.Integer,nullable=False,default=0)
    category=db.Column(db.String(),nullable=False,default='Starter')
    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.max_score}')"

class Question(db.Model, UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    question=db.Column(db.String(),nullable=False)
    option1=db.Column(db.String(),nullable=False)
    option2=db.Column(db.String(),nullable=False)
    option3=db.Column(db.String(),nullable=False)
    option4=db.Column(db.String(),nullable=False)
    correct_option=db.Column(db.String(),nullable=False)
    category=db.Column(db.String(),nullable=False)
    def __repr__(self):
        return f"Question('{self.question}','{self.correct_option} : {self.category}')"
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))