from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    api_key = StringField('API_Key', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Start')