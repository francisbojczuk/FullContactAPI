from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email

class IndexForm(FlaskForm):
    file = StringField('File:', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    api_key = StringField('API_KEY', validators=[DataRequired()])
    submit = SubmitField('Submit')
