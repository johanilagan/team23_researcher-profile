from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, current_app
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
from .forms import LoginForm, RegisterForm, EditProfileForm, UploadPaperForm
from .models import User, Profile, Social, Publication, File
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
    
    # Get user's publications (papers)
    publications = Publication.query.filter_by(pid=profile.pid).order_by(Publication.created_at.desc()).limit(3).all()
    
    return render_template("profile_page.html", researcher=user, is_owner=True, publications=publications)

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
    
    # Get researcher's publications (papers)
    publications = Publication.query.filter_by(pid=profile.pid).order_by(Publication.created_at.desc()).limit(3).all()
    
    return render_template("profile_page.html", researcher=researcher, is_owner=is_owner, publications=publications)

@main.route("/search")
def search():
    q = request.args.get("q", "").strip()
    
    # Basic query: adjust to your ORM/search logic
    if q:
        results = User.query.filter(
            (User.first_name.ilike(f"%{q}%")) |
            (User.last_name.ilike(f"%{q}%")) |
            (User.institution.ilike(f"%{q}%")) |
            (User.position.ilike(f"%{q}%"))
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
            current_user.institution = form.institution.data
            current_user.position = form.position.data
            
            # Get or create Profile record
            profile = Profile.query.filter_by(user_id=current_user.id).first()
            if not profile:
                profile = Profile(user_id=current_user.id)
                db.session.add(profile)
            
            # Update Profile table fields
            profile.name = f"{form.first_name.data} {form.last_name.data}"
            profile.institution = form.institution.data
            profile.bio = form.bio.data
            profile.location = form.location.data
            
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
            flash("Profile updated successfully!", "success")
            return redirect(url_for("main.my_profile"))
            
        except Exception as e:
            db.session.rollback()
            flash("An error occurred while updating your profile. Please try again.", "danger")
    
    # Pre-populate form with current data
    if request.method == "GET":
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.institution.data = current_user.institution
        form.position.data = current_user.position
        
        # Get profile data
        profile = Profile.query.filter_by(user_id=current_user.id).first()
        if profile:
            form.bio.data = profile.bio
            form.location.data = profile.location
            
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
        flash("Please check the form for errors and try again.", "danger")
    
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
            
            flash("Paper uploaded successfully!", "success")
            return redirect(url_for("main.my_profile"))
            
        except Exception as e:
            db.session.rollback()
            print(f"Error uploading paper: {str(e)}")
            import traceback
            traceback.print_exc()  # Print full traceback for debugging
            flash(f"An error occurred while uploading your paper: {str(e)}", "danger")
    
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

@main.route("/download/<filename>")
@login_required
def download_file(filename):
    """Securely serve uploaded files"""
    try:
        # Verify the file belongs to the current user
        profile = Profile.query.filter_by(user_id=current_user.id).first()
        if not profile:
            flash("Profile not found", "error")
            return redirect(url_for("main.my_profile"))
        
        file_record = File.query.filter_by(file_path=filename, pid=profile.pid).first()
        if not file_record:
            flash("File not found or access denied", "error")
            return redirect(url_for("main.my_profile"))
        
        file_path = os.path.join(current_app.root_path, 'static', 'uploads', filename)
        if os.path.exists(file_path):
            return redirect(url_for('static', filename='uploads/' + filename))
        else:
            flash("File not found on server", "error")
            return redirect(url_for("main.my_profile"))
            
    except Exception as e:
        print(f"Error serving file: {str(e)}")
        flash("Error accessing file", "error")
        return redirect(url_for("main.my_profile"))

@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for("main.home"))
        flash("Invalid credentials", "danger")
    return render_template("login.html", form=form)

@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # check if email already exists
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash("Email already registered. Please login.", "warning")
            return redirect(url_for("auth.register"))
        
        # create new user
        user = User(
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            institution=form.institution.data,
            position=form.position.data
        )
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash("Account created! Please login.", "success")
        return redirect(url_for("auth.login"))
    return render_template("register.html", form=form)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("main.home"))
