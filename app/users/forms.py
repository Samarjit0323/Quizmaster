from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User
from flask_wtf.file import FileField, FileAllowed

class regForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=10)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=7)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    def validate_username(self, username):
        user=User.query.filter_by(username=username.data).first()
        if user: #non-unique username
            raise ValidationError('Username already exists! Please choose a different one.')
    def validate_email(self, email):
        user=User.query.filter_by(email=email.data).first()
        if user: #non-unique email
            raise ValidationError('Email already exists! Please choose a different one.')

class loginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=7)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class updateProfile(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=10)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    profile_pic = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png','jpeg'])])
    submit = SubmitField('Update Profile')
    def validate_username(self, username):
        if username.data != current_user.username:
            existing_user=User.query.filter_by(username=username.data).first()
            if existing_user: #non-unique username
                raise ValidationError('Username already exists! Please choose a different one.')
    def validate_email(self, email):
        if email.data != current_user.email:
            existing_user=User.query.filter_by(email=email.data).first()
            if existing_user:
                raise ValidationError('Email already exists! Please choose a different one.')