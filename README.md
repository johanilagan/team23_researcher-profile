## Research'D (Academic Researcher Profiles)

Research'D is a Flask-based web application designed to connect researchers.  
Users can create academic profiles, upload publications, list research interests, and more.  

It supports:
- Researcher profiles with photo, institution, and bio
- Uploading and viewing publications
- Managing research interests
- Drag-and-drop reordering of profile sections
- Owner-only actions (edit profile, upload paper, logout)

## Features

- **Authentication**: User registration, login, and logout
- **Profile Management**: Edit profile info
- **Research Interests**: Add/remove interests with a searchable modal
- **Publications**: Upload PDFs, add metadata (authors, year, journal, etc.)
- **Dynamic Layout**: Drag-and-drop profile sections 
- **Access Control**: Edit/Logout buttons only visible to profile owners


## Tech

- **Backend**: Flask (Python), SQLAlchemy
- **Frontend**: Jinja2 templates, Bootstrap 5, SortableJS
- **Database**: SQLite (development) / PostgreSQL (production-ready)
- **Authentication**: Flask-Login
- **File Storage**: 

## Setup

1. First install the requirements by running
`pip install -r requirements.txt`
in your terminal
2. Run the programe by running 
`python app.py`
in your terminal.
