from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, URLField, DateField, IntegerField, SelectField
from wtforms.validators import InputRequired, Length, Email, EqualTo, Optional, NumberRange, DataRequired

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

    institution = SelectField("Institution", choices=[], validators=[InputRequired(message="Please select an institution")])
    position = SelectField("Position", choices=[], validators=[InputRequired(message="Please select position")])

    submit = SubmitField("Register")

class EditProfileForm(FlaskForm):
    first_name = StringField("First Name", validators=[InputRequired(), Length(min=1, max=100)])
    last_name = StringField("Last Name", validators=[InputRequired(), Length(min=1, max=100)])
    institution = StringField("Institution", validators=[Optional(), Length(max=150)])
    position = StringField("Position", validators=[Optional(), Length(max=100)])
    bio = TextAreaField("Bio", validators=[Optional(), Length(max=1000)])
    location = StringField("Location", validators=[Optional(), Length(max=150)])
    title = StringField("Title", validators=[Optional(), Length(max=150)])
    department = StringField("Department", validators=[Optional(), Length(max=150)])
    
    # Social media links
    linkedin_url = URLField("LinkedIn URL", validators=[Optional()])
    twitter_url = URLField("Twitter URL", validators=[Optional()])
    instagram_url = URLField("Instagram URL", validators=[Optional()])
    github_url = URLField("GitHub URL", validators=[Optional()])
    
    submit = SubmitField("Save Changes")

ACHIEVEMENT_TYPES = ['Award', 'Grant', 'Funds', 'Other']

class AchievementForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    type = SelectField("Type", choices=[(t, t) for t in ACHIEVEMENT_TYPES], validators=[DataRequired()])
    year = IntegerField("Year")
    description = TextAreaField("Description")

class UploadPaperForm(FlaskForm):
    title = StringField("Paper Title", validators=[InputRequired(), Length(min=1, max=300)])
    authors = TextAreaField("Authors", validators=[InputRequired(), Length(min=1, max=1000)], 
                           render_kw={"placeholder": "Enter author names separated by commas (e.g., John Smith, Jane Doe, etc.)"})
    journal = StringField("Journal/Conference", validators=[Optional(), Length(max=200)])
    publication_date = DateField("Publication Date", validators=[Optional()])
    year = IntegerField("Publication Year", validators=[Optional(), NumberRange(min=1900, max=2030)])
    doi = StringField("DOI", validators=[Optional(), Length(max=120)], 
                     render_kw={"placeholder": "e.g., 10.1234/example.doi"})
    url = URLField("External URL", validators=[Optional()], 
                  render_kw={"placeholder": "Link to paper on journal website or preprint server"})
    abstract = TextAreaField("Abstract", validators=[Optional(), Length(max=2000)], 
                            render_kw={"rows": 5, "placeholder": "Brief summary of the paper (optional)"})
    keywords = StringField("Keywords", validators=[Optional(), Length(max=500)], 
                          render_kw={"placeholder": "Enter keywords separated by commas"})
    paper_file = FileField("Upload Paper (PDF)", validators=[
        InputRequired(), FileAllowed(['pdf'], 'Only PDF files are allowed!')
    ])
    submit = SubmitField("Upload Paper")

class EditPaperForm(FlaskForm):
    title = StringField("Paper Title", validators=[InputRequired(), Length(min=1, max=300)])
    authors = TextAreaField("Authors", validators=[InputRequired(), Length(min=1, max=1000)], 
                           render_kw={"placeholder": "Enter author names separated by commas (e.g., John Smith, Jane Doe, etc.)"})
    journal = StringField("Journal/Conference", validators=[Optional(), Length(max=200)])
    publication_date = DateField("Publication Date", validators=[Optional()])
    year = IntegerField("Publication Year", validators=[Optional(), NumberRange(min=1900, max=2030)])
    doi = StringField("DOI", validators=[Optional(), Length(max=120)], 
                     render_kw={"placeholder": "e.g., 10.1234/example.doi"})
    url = URLField("External URL", validators=[Optional()], 
                  render_kw={"placeholder": "Link to paper on journal website or preprint server"})
    abstract = TextAreaField("Abstract", validators=[Optional(), Length(max=2000)], 
                            render_kw={"rows": 5, "placeholder": "Brief summary of the paper (optional)"})
    keywords = StringField("Keywords", validators=[Optional(), Length(max=500)], 
                          render_kw={"placeholder": "Enter keywords separated by commas"})
    paper_file = FileField("Update Paper (PDF)", validators=[
        Optional(), FileAllowed(['pdf'], 'Only PDF files are allowed!')
    ])
    submit = SubmitField("Update Paper")