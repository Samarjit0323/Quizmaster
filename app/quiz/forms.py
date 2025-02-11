from random import choices
from flask_wtf import FlaskForm  # Correct import
from wtforms import BooleanField, SubmitField, RadioField  # Correct BooleanField usage
from wtforms.validators import ValidationError, DataRequired  # Correct ValidationError import

class CorrectOption(FlaskForm):  # Correct class name capitalization
    options= RadioField("Choose the correct option:",choices=[])
    submit=SubmitField("Submit")
    def validate_options(self,options):
        if not options.data:
            raise ValidationError("Select an answer to proceed!")

class OptCategory(FlaskForm):
    options= RadioField("Choose a category", choices=[]) 
    submit=SubmitField("Submit")
    def validate_options(self,options):
        if not options.data:
            raise ValidationError("Select an answer to proceed!")