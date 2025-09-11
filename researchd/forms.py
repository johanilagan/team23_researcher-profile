from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, URLField
from wtforms.validators import InputRequired, Length, Email, EqualTo, Optional

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Email(), Length(max=150)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=4)])
    submit = SubmitField("Sign In")

class RegisterForm(FlaskForm):
    first_name = StringField("First Name", validators=[InputRequired(), Length(min=1, max=100)])
    last_name = StringField("Last Name", validators=[InputRequired(), Length(min=1, max=100)])

    email = StringField("Email", validators=[InputRequired(), Email(), Length(max=150)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=4, message="Password must be at least 4 characters long")])
    confirm_password = PasswordField("Confirm Password", validators=[InputRequired(), EqualTo("password", message="Passwords must match")])

    institution = StringField("Institution", validators=[Length(max=150)])
    position = StringField("Position", validators=[Length(max=100)])

    submit = SubmitField("Register")

class EditProfileForm(FlaskForm):
    first_name = StringField("First Name", validators=[InputRequired(), Length(min=1, max=100)])
    last_name = StringField("Last Name", validators=[InputRequired(), Length(min=1, max=100)])
    institution = StringField("Institution", validators=[Optional(), Length(max=150)])
    position = StringField("Position", validators=[Optional(), Length(max=100)])
    bio = TextAreaField("Bio", validators=[Optional(), Length(max=1000)])
    location = StringField("Location", validators=[Optional(), Length(max=150)])
    
    # Social media links
    linkedin_url = URLField("LinkedIn URL", validators=[Optional()])
    twitter_url = URLField("Twitter URL", validators=[Optional()])
    instagram_url = URLField("Instagram URL", validators=[Optional()])
    github_url = URLField("GitHub URL", validators=[Optional()])
    
    submit = SubmitField("Save Changes")
