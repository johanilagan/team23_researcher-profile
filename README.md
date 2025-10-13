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

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd researchd
   ```
2. **(Optional) Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate        # Mac/Linux
   venv\Scripts\activate           # Windows
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Apply database migrations**
   ```bash
   flask db upgrade
   ```
5. **(Optional) Populate the database with sample data**
   ```bash
   flask seed
   ```
6. **Run the application**
   You can run it using either Flask CLI or direct Python:
   **Option A — Flask CLI**
   ```bash
   flask run
   ```
   **Option B — Python directly**
   ```bash
   python app.py
   ```
   The app will start at: http://localhost:5000

## Group Members

| Name            | Student Number |
|-----------------|----------------|
| Elijah Thomson  | 23772983       |
| Austin Ngo      | 23801606       |
| Sepehr Amid     | 23342221       |
| Johan Illagan   | 23832843       |
| Rohma Rehman    | 23845362       |
| Annabelle Tiew  | 24028292       |

---

## Credits & Tools Used

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

## Favicon Attribution

Graduation cap icons created by Freepik - Flaticon  
Source: https://www.flaticon.com/free-icons/graduation-cap

License: Free for personal and commercial use with attribution

