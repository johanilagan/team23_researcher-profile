from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, URLField, DateField, IntegerField, SelectField
from wtforms.validators import InputRequired, Length, Email, EqualTo, Optional, NumberRange, DataRequired

# Title options for researchers
TITLE_CHOICES = [
    ('', 'Select Title (Optional)'),
    ('Mr', 'Mr'),
    ('Ms', 'Ms'),
    ('Mrs', 'Mrs'),
    ('Miss', 'Miss'),
    ('Dr', 'Dr'),
    ('Prof', 'Prof'),
    ('Assoc Prof', 'Assoc Prof'),
    ('Asst Prof', 'Asst Prof'),
    ('Prof Dr', 'Prof Dr'),
    ('Rev', 'Rev'),
    ('Other', 'Other')
]

# Position options for researchers
POSITION_CHOICES = [
    ('', 'Select Position'),
    ('Undergraduate Student', 'Undergraduate Student'),
    ('Postgraduate Student', 'Postgraduate Student'),
    ('PhD Candidate', 'PhD Candidate'),
    ('Research Assistant', 'Research Assistant'),
    ('Research Associate', 'Research Associate'),
    ('Postdoctoral Researcher', 'Postdoctoral Researcher'),
    ('Lecturer', 'Lecturer'),
    ('Senior Lecturer', 'Senior Lecturer'),
    ('Associate Professor', 'Associate Professor'),
    ('Professor', 'Professor'),
    ('Emeritus Professor', 'Emeritus Professor'),
    ('Adjunct Professor', 'Adjunct Professor'),
    ('Visiting Professor', 'Visiting Professor'),
    ('Research Fellow', 'Research Fellow'),
    ('Senior Research Fellow', 'Senior Research Fellow'),
    ('Principal Research Fellow', 'Principal Research Fellow'),
    ('Research Scientist', 'Research Scientist'),
    ('Senior Research Scientist', 'Senior Research Scientist'),
    ('Lab Manager', 'Lab Manager'),
    ('Department Head', 'Department Head'),
    ('Dean', 'Dean'),
    ('Other', 'Other (Not Listed)')
]

# Australian institution options
INSTITUTION_CHOICES = [
    ('', 'Select Institution'),
    ('Australian Catholic University', 'Australian Catholic University'),
    ('Australian National University', 'Australian National University'),
    ('Avondale University', 'Avondale University'),
    ('Bond University', 'Bond University'),
    ('Central Queensland University', 'Central Queensland University'),
    ('Charles Darwin University', 'Charles Darwin University'),
    ('Charles Sturt University', 'Charles Sturt University'),
    ('Curtin University', 'Curtin University'),
    ('Deakin University', 'Deakin University'),
    ('Edith Cowan University', 'Edith Cowan University'),
    ('Federation University Australia', 'Federation University Australia'),
    ('Flinders University', 'Flinders University'),
    ('Griffith University', 'Griffith University'),
    ('James Cook University', 'James Cook University'),
    ('La Trobe University', 'La Trobe University'),
    ('Macquarie University', 'Macquarie University'),
    ('Monash University', 'Monash University'),
    ('Murdoch University', 'Murdoch University'),
    ('Queensland University of Technology', 'Queensland University of Technology'),
    ('RMIT University', 'RMIT University'),
    ('Southern Cross University', 'Southern Cross University'),
    ('Swinburne University of Technology', 'Swinburne University of Technology'),
    ('Torrens University Australia', 'Torrens University Australia'),
    ('University of Adelaide', 'University of Adelaide'),
    ('University of Canberra', 'University of Canberra'),
    ('University of Divinity', 'University of Divinity'),
    ('University of Melbourne', 'University of Melbourne'),
    ('University of New England', 'University of New England'),
    ('University of New South Wales', 'University of New South Wales'),
    ('University of Newcastle', 'University of Newcastle'),
    ('University of Notre Dame Australia', 'University of Notre Dame Australia'),
    ('University of Queensland', 'University of Queensland'),
    ('University of South Australia', 'University of South Australia'),
    ('University of Southern Queensland', 'University of Southern Queensland'),
    ('University of Sydney', 'University of Sydney'),
    ('University of Tasmania', 'University of Tasmania'),
    ('University of Technology Sydney', 'University of Technology Sydney'),
    ('University of the Sunshine Coast', 'University of the Sunshine Coast'),
    ('University of Western Australia', 'University of Western Australia'),
    ('University of Wollongong', 'University of Wollongong'),
    ('Victoria University', 'Victoria University'),
    ('Western Sydney University', 'Western Sydney University'),
    ('Other', 'Other (Not Listed)')
]

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Email(), Length(max=150)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=4)])
    submit = SubmitField("Sign In")

class RegisterForm(FlaskForm):
    title = SelectField("Title", choices=TITLE_CHOICES, validators=[Optional()])
    first_name = StringField("First Name", validators=[InputRequired(), Length(min=1, max=100)])
    last_name = StringField("Last Name", validators=[InputRequired(), Length(min=1, max=100)])

    email = StringField("Email", validators=[InputRequired(), Email(), Length(max=150)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=4, message="Password must be at least 4 characters long")])
    confirm_password = PasswordField("Confirm Password", validators=[InputRequired(), EqualTo("password", message="Passwords must match")])

    institution = SelectField("Institution", choices=INSTITUTION_CHOICES, validators=[Optional()])
    other_institution = StringField("Other Institution (if not listed)", validators=[Optional(), Length(max=150)])
    position = SelectField("Position", choices=POSITION_CHOICES, validators=[Optional()])
    other_position = StringField("Other Position (if not listed)", validators=[Optional(), Length(max=100)])

    submit = SubmitField("Register")

class EditProfileForm(FlaskForm):
    title = SelectField("Title", choices=TITLE_CHOICES, validators=[Optional()])
    first_name = StringField("First Name", validators=[InputRequired(), Length(min=1, max=100)])
    last_name = StringField("Last Name", validators=[InputRequired(), Length(min=1, max=100)])
    institution = SelectField("Institution", choices=INSTITUTION_CHOICES, validators=[Optional()])
    other_institution = StringField("Other Institution (if not listed)", validators=[Optional(), Length(max=150)])
    position = SelectField("Position", choices=POSITION_CHOICES, validators=[Optional()])
    other_position = StringField("Other Position (if not listed)", validators=[Optional(), Length(max=100)])
    bio = TextAreaField("Bio", validators=[Optional(), Length(max=1000)])
    location = StringField("Location", validators=[Optional(), Length(max=150)])
    department = StringField("Department", validators=[Optional(), Length(max=150)])
    
    # Profile picture
    profile_picture = FileField("Profile Picture", validators=[
        Optional(), FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Only image files (JPG, PNG, GIF) are allowed!')
    ])
    
    # Social media links
    linkedin_url = URLField("LinkedIn URL", validators=[Optional()])
    twitter_url = URLField("X (Twitter) URL", validators=[Optional()])
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