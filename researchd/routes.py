import json
from flask import Blueprint, render_template, redirect, url_for, request, jsonify, current_app, send_from_directory
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
from .forms import LoginForm, RegisterForm, EditProfileForm, UploadPaperForm, EditPaperForm
from .models import User, Profile, Social, Publication, File
from sqlalchemy.orm import joinedload
from . import db
import os
from datetime import datetime

auth = Blueprint("auth", __name__)
main = Blueprint("main", __name__)

@main.route("/")
def home():
    return render_template("homepage.html")

@main.route("/profile")
@login_required
def my_profile():
    # Get fresh user data with profile
    user = User.query.get(current_user.id)
    
    # Ensure profile exists for current user
    profile = Profile.query.filter_by(user_id=user.id).first()
    if not profile:
        profile = Profile(user_id=user.id)
        db.session.add(profile)
        db.session.commit()
    
    print(f"Loading profile for user {user.id}, interests: {profile.research_interests}")

    # Sets default order for sections
    default_sections = ['profile-header', 'interests-section', 'papers-section']
    if profile.section_order:
        try:
            section_order = json.loads(profile.section_order)
            if not section_order:
                section_order = default_sections
        except Exception:
            section_order = default_sections
    else:
        section_order = default_sections
    
    # Get user's publications (papers)
    publications = Publication.query.filter_by(pid=profile.pid).order_by(Publication.created_at.desc()).limit(3).all()
    
    return render_template("profile_page.html", profile=profile, is_owner=True, publications=publications, section_order=section_order)

@main.route("/profile/<int:researcher_id>")
def researcher_profile(researcher_id):
    researcher = User.query.get(researcher_id)
    if not researcher:
        from flask import abort
        abort(404)
    
    is_owner = current_user.is_authenticated and current_user.id == researcher.id
    
    # Ensure profile exists for the researcher
    profile = Profile.query.filter_by(user_id=researcher.id).first()
    if not profile:
        profile = Profile(user_id=researcher.id)
        db.session.add(profile)
        db.session.commit()

    # Sets default order for sections
    default_sections = ['profile-header', 'interests-section', 'papers-section']
    if profile.section_order:
        try:
            section_order = json.loads(profile.section_order)
            if not section_order:
                section_order = default_sections
        except Exception:
            section_order = default_sections
    else:
        section_order = default_sections
    
    # Get researcher's publications (papers)
    publications = Publication.query.filter_by(pid=profile.pid).order_by(Publication.created_at.desc()).limit(3).all()
    
    return render_template("profile_page.html", profile=profile, is_owner=is_owner, publications=publications, section_order=section_order)

@main.route("/search")
def search():
    q = request.args.get("q", "").strip()
    
    # Basic query: adjust to your ORM/search logic
    if q:
        results = User.query.join(Profile).options(joinedload(User.profile)).filter(
            (User.first_name.ilike(f"%{q}%")) |
            (User.last_name.ilike(f"%{q}%")) |
            (Profile.institution.ilike(f"%{q}%")) |
            (Profile.position.ilike(f"%{q}%"))
        ).all()
    else:
        results = User.query.all()  # show all users if no query

    return render_template("search.html", results=results, q=q)

@main.route("/help")
def help():
    return render_template("help_centre.html")

@main.route("/contact")
def contact():
    return render_template("contact.html")

@main.route("/privacy")
def privacy():
    return render_template("privacy.html")

@main.route("/edit-profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm()
    
    if form.validate_on_submit():
        try:
            # Update User table fields
            current_user.first_name = form.first_name.data
            current_user.last_name = form.last_name.data
            
            # Get or create Profile record
            profile = Profile.query.filter_by(user_id=current_user.id).first()
            if not profile:
                profile = Profile(user_id=current_user.id)
                db.session.add(profile)
            
            # Update Profile table fields
            profile.institution = form.institution.data
            profile.position = form.position.data
            profile.bio = form.bio.data
            profile.location = form.location.data
            profile.title = form.title.data
            profile.department = form.department.data

            
            # Update social media links
            social_platforms = {
                'LinkedIn': form.linkedin_url.data,
                'Twitter': form.twitter_url.data,
                'Instagram': form.instagram_url.data,
                'GitHub': form.github_url.data
            }
            
            for platform, url in social_platforms.items():
                if url:  # Only add if URL is provided
                    social = Social.query.filter_by(pid=profile.pid, platform=platform).first()
                    if social:
                        social.url = url
                    else:
                        social = Social(pid=profile.pid, platform=platform, url=url)
                        db.session.add(social)
                else:
                    # Remove social link if URL is empty
                    social = Social.query.filter_by(pid=profile.pid, platform=platform).first()
                    if social:
                        db.session.delete(social)
            
            db.session.commit()
            return redirect(url_for("main.my_profile"))
            
        except Exception as e:
            db.session.rollback()
            pass
    
    # Pre-populate form with current data
    if request.method == "GET":
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        
        # Get profile data
        profile = Profile.query.filter_by(user_id=current_user.id).first()
        if profile:
            form.bio.data = profile.bio
            form.location.data = profile.location
            form.title.data = profile.title
            form.department.data = profile.department
            form.institution.data = profile.institution
            form.position.data = profile.position
            
            # Get social media links
            socials = {s.platform: s.url for s in profile.socials}
            form.linkedin_url.data = socials.get('LinkedIn', '')
            form.twitter_url.data = socials.get('Twitter', '')
            form.instagram_url.data = socials.get('Instagram', '')
            form.github_url.data = socials.get('GitHub', '')
    
    return render_template("edit_profile.html", form=form)

@main.route("/update-interests", methods=["POST"])
@login_required
def update_interests():
    try:
        data = request.get_json()
        interests = data.get('interests', '')
        
        print(f"Updating interests for user {current_user.id}: {interests}")
        
        # Get or create profile
        profile = Profile.query.filter_by(user_id=current_user.id).first()
        if not profile:
            profile = Profile(user_id=current_user.id)
            db.session.add(profile)
        
        # Update research interests
        profile.research_interests = interests
        db.session.commit()
        
        print(f"Interests saved successfully: {profile.research_interests}")
        return jsonify({'success': True})
        
    except Exception as e:
        db.session.rollback()
        print(f"Error updating interests: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@main.route("/upload-paper", methods=["GET", "POST"])
@login_required
def upload_paper():
    form = UploadPaperForm()
    
    # Debug: Print form errors if validation fails
    if request.method == "POST" and not form.validate_on_submit():
        print("Form validation failed!")
        for field, errors in form.errors.items():
            print(f"Field '{field}': {errors}")
        pass
    
    if form.validate_on_submit():
        try:
            # Get or create profile
            profile = Profile.query.filter_by(user_id=current_user.id).first()
            if not profile:
                profile = Profile(user_id=current_user.id)
                db.session.add(profile)
                db.session.commit()
            
            # Handle file upload
            uploaded_file = None
            if form.paper_file.data:
                file = form.paper_file.data
                if file and file.filename:
                    # Create uploads directory if it doesn't exist
                    upload_dir = os.path.join(current_app.root_path, 'static', 'uploads')
                    os.makedirs(upload_dir, exist_ok=True)
                    
                    # Generate secure filename
                    filename = secure_filename(file.filename)
                    # Add timestamp to avoid conflicts
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
                    filename = timestamp + filename
                    filepath = os.path.join(upload_dir, filename)
                    
                    # Save file
                    file.save(filepath)
                    
                    # Get file size
                    file_size = os.path.getsize(filepath)
                    
                    # Create File record
                    uploaded_file = File(
                        pid=profile.pid,
                        file_name=file.filename,
                        file_type='pdf',
                        file_size=file_size,
                        file_path=filename  # Store relative path
                    )
                    db.session.add(uploaded_file)
                    db.session.flush()  # Get the file ID
            
            # Create Publication record
            publication = Publication(
                pid=profile.pid,
                title=form.title.data,
                authors=form.authors.data,
                journal=form.journal.data,
                year=form.year.data,
                publication_date=form.publication_date.data,
                doi=form.doi.data,
                url=form.url.data,
                abstract=form.abstract.data,
                keywords=form.keywords.data
            )
            
            # Link to uploaded file if available
            if uploaded_file:
                publication.fid = uploaded_file.fid
            
            db.session.add(publication)
            db.session.commit()
            
            return redirect(url_for("main.my_profile"))
            
        except Exception as e:
            db.session.rollback()
            print(f"Error uploading paper: {str(e)}")
            import traceback
            traceback.print_exc()  # Print full traceback for debugging
            pass
    
    return render_template("upload_paper.html", form=form)

@main.route("/papers")
@login_required
def my_papers():
    """Display user's uploaded papers"""
    profile = Profile.query.filter_by(user_id=current_user.id).first()
    if not profile:
        profile = Profile(user_id=current_user.id)
        db.session.add(profile)
        db.session.commit()
    
    papers = Publication.query.filter_by(pid=profile.pid).order_by(Publication.created_at.desc()).all()
    return render_template("my_papers.html", papers=papers)

@main.route("/paper/<int:paper_id>")
def paper_detail(paper_id):
    paper = Publication.query.get_or_404(paper_id)
    return render_template("paper_detail.html", paper=paper)

@main.route("/edit-paper/<int:paper_id>", methods=["GET", "POST"])
@login_required
def edit_paper(paper_id):
    """Edit an existing paper"""
    # Get the paper and verify ownership
    profile = Profile.query.filter_by(user_id=current_user.id).first()
    if not profile:
        return redirect(url_for("main.my_papers"))
    
    paper = Publication.query.filter_by(pubid=paper_id, pid=profile.pid).first()
    if not paper:
        return redirect(url_for("main.my_papers"))
    
    form = EditPaperForm()
    
    # Debug: Print form errors if validation fails
    if request.method == "POST" and not form.validate_on_submit():
        print("Form validation failed!")
        for field, errors in form.errors.items():
            print(f"Field '{field}': {errors}")
        pass
    
    if form.validate_on_submit():
        try:
            # Update paper fields
            paper.title = form.title.data
            paper.authors = form.authors.data
            paper.journal = form.journal.data
            paper.year = form.year.data
            paper.publication_date = form.publication_date.data
            paper.doi = form.doi.data
            paper.url = form.url.data
            paper.abstract = form.abstract.data
            paper.keywords = form.keywords.data
            
            # Handle file upload if provided
            if form.paper_file.data:
                file = form.paper_file.data
                if file and file.filename:
                    # Create uploads directory if it doesn't exist
                    upload_dir = os.path.join(current_app.root_path, 'static', 'uploads')
                    os.makedirs(upload_dir, exist_ok=True)
                    
                    # Generate secure filename
                    filename = secure_filename(file.filename)
                    # Add timestamp to avoid conflicts
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
                    filename = timestamp + filename
                    filepath = os.path.join(upload_dir, filename)
                    
                    # Save file
                    file.save(filepath)
                    
                    # Get file size
                    file_size = os.path.getsize(filepath)
                    
                    # Delete old file if it exists
                    if paper.file:
                        old_file_path = os.path.join(upload_dir, paper.file.file_path)
                        if os.path.exists(old_file_path):
                            os.remove(old_file_path)
                        db.session.delete(paper.file)
                    
                    # Create new File record
                    new_file = File(
                        pid=profile.pid,
                        file_name=file.filename,
                        file_type='pdf',
                        file_size=file_size,
                        file_path=filename  # Store relative path
                    )
                    db.session.add(new_file)
                    db.session.flush()  # Get the file ID
                    
                    # Update paper to link to new file
                    paper.fid = new_file.fid
            
            db.session.commit()
            return redirect(url_for("main.my_papers"))
            
        except Exception as e:
            db.session.rollback()
            print(f"Error updating paper: {str(e)}")
            import traceback
            traceback.print_exc()  # Print full traceback for debugging
            pass
    
    # Pre-populate form with current data
    if request.method == "GET":
        form.title.data = paper.title
        form.authors.data = paper.authors
        form.journal.data = paper.journal
        form.year.data = paper.year
        form.publication_date.data = paper.publication_date
        form.doi.data = paper.doi
        form.url.data = paper.url
        form.abstract.data = paper.abstract
        form.keywords.data = paper.keywords
    
    return render_template("edit_paper.html", form=form, paper=paper)

@main.route("/download/<filename>")
@login_required
def download_file(filename):
    """Securely serve uploaded files with option to preview inline"""
    try:
        # Verify the file belongs to the current user
        profile = Profile.query.filter_by(user_id=current_user.id).first()
        if not profile:
            return redirect(url_for("main.my_profile"))
        
        file_record = File.query.filter_by(file_path=filename, pid=profile.pid).first()
        if not file_record:
            return redirect(url_for("main.my_profile"))
        
        file_path = os.path.join(current_app.root_path, 'static', 'uploads')
        if os.path.exists(os.path.join(file_path, filename)):
            # Use send_from_directory with as_attachment=False to preview inline
            return send_from_directory(file_path, filename, as_attachment=False, mimetype='application/pdf')
        else:
            return redirect(url_for("main.my_profile"))
            
    except Exception as e:
        print(f"Error serving file: {str(e)}")
        return redirect(url_for("main.my_profile"))

@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for("main.home"))
    return render_template("login.html", form=form)

@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # check if email already exists
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            return redirect(url_for("auth.register"))
        
        # create new user
        user = User(
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
        )
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        profile = Profile(
            user_id=user.id,
            institution=form.institution.data,
            position=form.position.data
        )

        db.session.add(profile)
        db.session.commit()

        return redirect(url_for("auth.login"))
    return render_template("register.html", form=form)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.home"))

@main.route("/save-section-order", methods=["POST"])
@login_required
def save_section_order():
    data = request.get_json()
    order = data.get("order")
    if not order or not isinstance(order, list):
        return jsonify({"success": False, "error": "Invalid order data"}), 400
    profile = Profile.query.filter_by(user_id=current_user.id).first()
    if not profile:
        return jsonify({"success": False, "error": "Profile not found"}), 404
    profile.section_order = json.dumps(order)
    db.session.commit()
    return jsonify({"success": True})