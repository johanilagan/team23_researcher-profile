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
- **Publications**: Upload PDFs, add metadata (authors, year, journal, etc.), keyword extract from paper
- **Dynamic Layout**: Drag-and-drop profile sections 
- **Access Control**: Edit/Logout buttons only visible to profile owners

## Tech

- **Backend**: Flask (Python), SQLAlchemy
- **Frontend**: Jinja2 templates, Bootstrap 5, SortableJS
- **Database**: SQLite (development) / PostgreSQL (production-ready)
- **Authentication**: Flask-Login
- **File Storage**: 

## Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- Git (for cloning repository)
- [Optional] Virtual environment tool (venv or virtualenv)

## Setup

1. First install the requirements by running
`pip install -r requirements.txt`
in your terminal
2. Run the programe by running 
`python app.py`
in your terminal.
The application will start on http://localhost:5000 by default. 

## Group Members

| Name        | Student Number              |
|-------------|------------------------------------|
| Elijah Thomson |23772983| 
| Austin Ngo     |23801606 |
| Sepehr Amid  |23342221|
| Johan Illagan  |23832843|
| Rohma Rehman   |23845362|
| Annabelle Tiew     |24028292|


---

##  Credits & Tools Used

### Languages & Frameworks
- Python (Flask) – Backend development  
- HTML, CSS, JavaScript – Frontend interface  
- Bootstrap 5 – Styling and responsive design  
- Jinja2 – Template engine  

### Libraries & Packages
- Flask-Login – Authentication  
- SQLAlchemy – ORM  
- WTForms – Form handling  
- SortableJS – Drag-and-drop functionality  

### Development & Collaboration Tools
- GitHub – Version control & collaboration  
- Git – Branching & pull requests  
- Visual Studio Code / PyCharm – IDEs  
- Figma – UI prototyping  

### Credits
- Bootstrap Icons & Font Awesome for icons  
- Placeholder images from [via.placeholder.com](https://via.placeholder.com)  
- Open-source libraries listed above  

Favicon Attribution
===================

Graduation cap icons created by Freepik - Flaticon
Source: https://www.flaticon.com/free-icons/graduation-cap

License: Free for personal and commercial use with attribution

