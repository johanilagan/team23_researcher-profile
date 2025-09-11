from flask.cli import with_appcontext
from researchd import db
from researchd.models import User, Profile, Education, Experience, File, Photo, Social, Publication
import click

@click.command("seed")
@with_appcontext
def seed():
    # Clears existing data
    db.drop_all()
    db.create_all()

    # Creates sample user
    user = User(
        email = "alice@example.com",
        first_name = "Alice",
        last_name = "Smith",
        institution = "Example University",
        position = "Professor"
    )
    user.set_password("password123")
    db.session.add(user)
    db.session.commit()

    # Creates sample profile
    profile = Profile(
        user_id = user.id,
        name = "Alice Smith",
        title = "Professor of Biology",
        institution = "Example University",
        department = "Biology",
        bio = "Researcher in molecular biology",
        pfp = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRHEJ-8GyKlZr5ZmEfRMmt5nR4tH_aP-crbgg&s",
        location = "Perth"
    )
    db.session.add(profile)
    db.session.commit()

    # Creates sample education
    edu = Education(
        pid = profile.pid,
        degree = "PhD in Biology",
        institution = "University of Western Australia",
        start_year = 2005,
        end_year = 2010
    )
    db.session.add(edu)

    # Creates sample experience
    exp = Experience(
        pid = profile.pid,
        role = "Research Scientist",
        institution = "BioLabs Inc.",
        start_year = 2010,
        end_year = 2015
    )
    db.session.add(exp)

    # Adds a sample file
    file = File(
        pid = profile.pid,
        file_name = "research_paper.pdf",
        file_type = "pdf",
        file_size = 123456,
        file_path = "https://frazer.uq.edu.au/files/3190/MolBiolWS01DNATech.pdf"
    )
    db.session.add(file)
    db.session.commit()

    # Adds sample publication
    pub = Publication(
        pid = profile.pid,
        title = "Groundbreaking Research",
        journal = "Science Journal",
        year = 2020,
        doi = "10.1234/example.doi",
        url = "https://doi.org/10.1234/example.doi",
        fid = file.fid
    )
    db.session.add(pub)

    # Adds sample photo
    photo = Photo(
        pid = profile.pid,
        file_path = "https://media.istockphoto.com/id/1089913166/photo/female-medical-researcher.jpg",
        caption = "Alice in a lab"
    )
    db.session.add(photo)

    # Adds sample social link
    social = Social(
        pid = profile.pid,
        platform = "Twitter",
        url = "https://twitter.com/alice"
    )
    db.session.add(social)

    db.session.commit()
    print("Sample data loaded.")