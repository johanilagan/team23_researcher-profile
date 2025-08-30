from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, Email

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Email(), Length(max=150)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=4)])
    submit = SubmitField("Sign In")

class RegisterForm(FlaskForm):
    first_name = StringField("First Name", validators=[InputRequired(), Length(min=1, max=100)])
    last_name = StringField("Last Name", validators=[InputRequired(), Length(min=1, max=100)])

    email = StringField("Email", validators=[InputRequired(), Email(), Length(max=150)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=4)])

    institution = StringField("Institution", validators=[Length(max=150)])
    position = StringField("Position", validators=[Length(max=100)])

    submit = SubmitField("Register")
