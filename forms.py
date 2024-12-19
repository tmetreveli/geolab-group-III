from flask_wtf import FlaskForm
from wtforms.fields import StringField, IntegerField, SubmitField, SelectField, IntegerField, FileField
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


class AddDogForm(FlaskForm):
    name = StringField(label='Enter name here', validators=[DataRequired()])
    img = FileField('Image', validators=[DataRequired(), Length(min=5, max=255)])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Add Dog')

class RegisterForm(FlaskForm):
    username = StringField(label='Enter name here', validators=[DataRequired(), Length(min=4, max=255)])
    password = PasswordField(label='Password', validators=[DataRequired()])
    repeat_password = PasswordField(label="Repeat Password", validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField(label='Enter name here', validators=[DataRequired(), Length(min=4, max=255)])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField('Login')