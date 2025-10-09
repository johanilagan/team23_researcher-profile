import json
from flask import Blueprint, render_template, redirect, url_for, request, jsonify, current_app, send_from_directory
from flask_login import login_user, login_required, logout_user, current_user
from flask_wtf.csrf import validate_csrf
from werkzeug.utils import secure_filename
from .forms import LoginForm, RegisterForm, EditProfileForm, UploadPaperForm, EditPaperForm
from .models import User, Profile, Social, Publication, File, Achievement, ExternalRole
from sqlalchemy.orm import joinedload
from . import db
import os
from datetime import datetime

auth = Blueprint("auth", __name__)
main = Blueprint("main", __name__)

def validate_csrf_token():
    """Validate CSRF token for AJAX requests"""
    try:
        validate_csrf(request.headers.get('X-CSRFToken'))
        return True
    except Exception:
        return False

@main.route("/")
def home():
    return render_template("homepage.html")

@main.route("/profile")
@login_required
def my_profile():
    print(">>> Running MY_PROFILE route <<<")
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
    default_sections = [
        {"section": 'profile-header', 'visible': True},
        {'section': 'interests-section', 'visible': True},
        {'section': 'papers-section', 'visible': True},
        {'section': 'achievements-section', 'visible': False},
        {'section': 'external-roles-section', 'visible': False}
    ]
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

    # Load external roles
    external_roles = ExternalRole.query.filter_by(pid=profile.pid).order_by(ExternalRole.sort_order.nulls_last(), ExternalRole.start_year.desc().nulls_last()).all()

    print("Loaded section_order:", section_order)
    for s in section_order:
        print(s['section'], s['visible'], type(s['visible']))
    
    return render_template("profile_page.html", profile=profile, is_owner=True, publications=publications, section_order=section_order, external_roles=external_roles)

@main.route("/profile/<int:researcher_id>")
def researcher_profile(researcher_id):
    print(f">>> Running RESEARCHER_PROFILE route for {researcher_id} <<<")
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
    default_sections = [
        {"section": 'profile-header', 'visible': True},
        {'section': 'interests-section', 'visible': True},
        {'section': 'papers-section', 'visible': True},
        {'section': 'achievements-section', 'visible': False},
        {'section': 'external-roles-section', 'visible': False}
    ]
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

    # Load external roles
    external_roles = ExternalRole.query.filter_by(pid=profile.pid).order_by(ExternalRole.sort_order.nulls_last(), ExternalRole.start_year.desc().nulls_last()).all()
    
    return render_template("profile_page.html", profile=profile, is_owner=is_owner, publications=publications, section_order=section_order, external_roles=external_roles)

@main.route("/search")
def search():
    q = request.args.get("q", "").strip()
    institution_filter = request.args.get("institution", "").strip()
    position_filter = request.args.get("position", "").strip()
    interests_filter = request.args.get("interests", "").strip()
    sort_by = request.args.get("sort", "name").strip()
    page = request.args.get("page", 1, type=int)
    per_page = 10  # 10 researchers per page
    
    # Start with base query
    query = User.query.join(Profile).options(joinedload(User.profile))
    
    # Apply search query
    if q:
        query = query.filter(
            (User.first_name.ilike(f"%{q}%")) |
            (User.last_name.ilike(f"%{q}%")) |
            (Profile.institution.ilike(f"%{q}%")) |
            (Profile.position.ilike(f"%{q}%")) |
            (Profile.research_interests.ilike(f"%{q}%"))
        )
    
    # Apply filters
    if institution_filter:
        query = query.filter(Profile.institution == institution_filter)
    
    if position_filter:
        query = query.filter(Profile.position == position_filter)
    
    if interests_filter:
        query = query.filter(Profile.research_interests.ilike(f"%{interests_filter}%"))
    
    # Apply sorting
    if sort_by == "institution":
        query = query.order_by(Profile.institution.asc())
    elif sort_by == "position":
        query = query.order_by(Profile.position.asc())
    else:  # default to name
        query = query.order_by(User.first_name.asc(), User.last_name.asc())
    
    # Apply pagination
    pagination = query.paginate(
        page=page, 
        per_page=per_page, 
        error_out=False
    )
    results = pagination.items
    
    # Get unique values for filter dropdowns
    institutions = db.session.query(Profile.institution).filter(Profile.institution.isnot(None), Profile.institution != "").distinct().all()
    institutions = [inst[0] for inst in institutions if inst[0]]
    
    positions = db.session.query(Profile.position).filter(Profile.position.isnot(None), Profile.position != "").distinct().all()
    positions = [pos[0] for pos in positions if pos[0]]
    
    # Get unique research interests (split by comma and get unique values)
    interests_query = db.session.query(Profile.research_interests).filter(Profile.research_interests.isnot(None), Profile.research_interests != "").all()
    interests = set()
    for interest_row in interests_query:
        if interest_row[0]:
            # Split by comma and add each interest
            for interest in interest_row[0].split(','):
                interests.add(interest.strip())
    interests = sorted(list(interests))

    return render_template("search.html", 
                         results=results, 
                         pagination=pagination,
                         q=q,
                         institution_filter=institution_filter,
                         position_filter=position_filter,
                         interests_filter=interests_filter,
                         sort_by=sort_by,
                         institutions=institutions,
                         positions=positions,
                         interests=interests)

@main.route("/help")
def help_centre():
    return render_template("help_centre.html")

@main.route("/privacy")
def privacy():
    return render_template("privacy.html")

@main.route("/edit-profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm()
    
    profile = Profile.query.filter_by(user_id=current_user.id).first()
    if not profile:
        profile = Profile(user_id=current_user.id)
        db.session.add(profile)
        db.session.flush()  # Ensures profile.pid is available for achievements/socials

    if form.validate_on_submit():
        try:
            # Update User fields
            current_user.first_name = form.first_name.data
            current_user.last_name = form.last_name.data

            # Update Profile fields
            profile.institution = form.institution.data
            profile.position = form.position.data
            profile.bio = form.bio.data
            profile.location = form.location.data
            profile.title = form.title.data
            profile.department = form.department.data

            # Handle profile picture upload
            if form.profile_picture.data:
                file = form.profile_picture.data
                if file and file.filename:
                    # Create profile_pics directory if it doesn't exist
                    upload_dir = os.path.join(current_app.root_path, 'static', 'profile_pics')
                    os.makedirs(upload_dir, exist_ok=True)
                    
                    # Generate secure filename
                    filename = secure_filename(file.filename)
                    # Add user ID and timestamp to avoid conflicts
                    file_ext = os.path.splitext(filename)[1]
                    filename = f"user_{current_user.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{file_ext}"
                    filepath = os.path.join(upload_dir, filename)
                    
                    # Delete old profile picture if it exists
                    if profile.pfp:
                        old_pic_path = os.path.join(current_app.root_path, 'static', profile.pfp)
                        if os.path.exists(old_pic_path):
                            try:
                                os.remove(old_pic_path)
                            except Exception as e:
                                print(f"Error removing old profile picture: {e}")
                    
                    # Save new file
                    file.save(filepath)
                    
                    # Store relative path in database
                    profile.pfp = f"profile_pics/{filename}"

            # Update social links
            social_platforms = {
                'LinkedIn': form.linkedin_url.data,
                'Twitter': form.twitter_url.data,
                'Instagram': form.instagram_url.data,
                'GitHub': form.github_url.data
            }

            for platform, url in social_platforms.items():
                social = Social.query.filter_by(pid=profile.pid, platform=platform).first()
                if url:
                    if social:
                        social.url = url
                    else:
                        db.session.add(Social(pid=profile.pid, platform=platform, url=url))
                elif social:
                    db.session.delete(social)

            db.session.commit()
            return redirect(url_for("main.my_profile"))

        except Exception as e:
            db.session.rollback()
            print(f"Error updating profile: {e}")

    elif request.method == "GET":
        # Pre-populate User fields
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name

        # Pre-populate Profile fields
        form.institution.data = profile.institution
        form.position.data = profile.position
        form.bio.data = profile.bio
        form.location.data = profile.location
        form.title.data = profile.title
        form.department.data = profile.department

        # Pre-populate social links
        socials = {s.platform: s.url for s in profile.socials}
        form.linkedin_url.data = socials.get('LinkedIn', '')
        form.twitter_url.data = socials.get('Twitter', '')
        form.instagram_url.data = socials.get('Instagram', '')
        form.github_url.data = socials.get('GitHub', '')

    return render_template("edit_profile.html", form=form, profile=profile)



@main.route("/update-interests", methods=["POST"])
@login_required
def update_interests():
    if not validate_csrf_token():
        return jsonify({'success': False, 'error': 'Invalid CSRF token'}), 400
    
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

@main.route("/upload-profile-picture", methods=["POST"])
@login_required
def upload_profile_picture():
    if not validate_csrf_token():
        return jsonify({'success': False, 'error': 'Invalid CSRF token'}), 400
    
    try:
        # Check if file was uploaded
        if 'profile_picture' not in request.files:
            return jsonify({'success': False, 'error': 'No file uploaded'}), 400
        
        file = request.files['profile_picture']
        
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        # Validate file extension
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
        if '.' not in file.filename:
            return jsonify({'success': False, 'error': 'Invalid file type'}), 400
        
        file_ext = file.filename.rsplit('.', 1)[1].lower()
        if file_ext not in allowed_extensions:
            return jsonify({'success': False, 'error': 'Only image files (JPG, PNG, GIF) are allowed'}), 400
        
        # Get or create profile
        profile = Profile.query.filter_by(user_id=current_user.id).first()
        if not profile:
            profile = Profile(user_id=current_user.id)
            db.session.add(profile)
            db.session.flush()
        
        # Create profile_pics directory if it doesn't exist
        upload_dir = os.path.join(current_app.root_path, 'static', 'profile_pics')
        os.makedirs(upload_dir, exist_ok=True)
        
        # Generate secure filename
        filename = f"user_{current_user.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{file_ext}"
        filepath = os.path.join(upload_dir, filename)
        
        # Delete old profile picture if it exists
        if profile.pfp:
            old_pic_path = os.path.join(current_app.root_path, 'static', profile.pfp)
            if os.path.exists(old_pic_path):
                try:
                    os.remove(old_pic_path)
                except Exception as e:
                    print(f"Error removing old profile picture: {e}")
        
        # Save new file
        file.save(filepath)
        
        # Store relative path in database
        profile.pfp = f"profile_pics/{filename}"
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'image_url': url_for('static', filename=profile.pfp)
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"Error uploading profile picture: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

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
    if not validate_csrf_token():
        return jsonify({'success': False, 'error': 'Invalid CSRF token'}), 400
    
    data = request.get_json()
    order = data.get("order")
    if not isinstance(order, list):
        return jsonify({'success': False, 'error': 'Invalid data'}), 400
    profile = Profile.query.filter_by(user_id=current_user.id).first()
    if not profile:
        return jsonify({'success': False, 'error': 'Profile not found'}), 400
    profile.section_order = json.dumps(order)
    db.session.commit()
    return jsonify({'success': True})


@main.route("/add_external_role", methods=["POST"])
@login_required
def add_external_role():
    if not validate_csrf_token():
        return jsonify({'success': False, 'error': 'Invalid CSRF token'}), 400
    
    try:
        data = request.get_json()
        role_title = data.get("role_title", "").strip()
        organization = data.get("organization", "").strip()
        start_year = data.get("start_year")
        end_year = data.get("end_year")
        description = data.get("description", "").strip()

        if not role_title or not organization:
            return jsonify({"success": False, "error": "role_title and organization are required"}), 400

        profile = Profile.query.filter_by(user_id=current_user.id).first()
        if not profile:
            profile = Profile(user_id=current_user.id)
            db.session.add(profile)
            db.session.flush()

        # Determine next sort order
        max_sort = db.session.query(db.func.max(ExternalRole.sort_order)).filter_by(pid=profile.pid).scalar()
        next_sort = (max_sort or 0) + 1

        er = ExternalRole(
            pid=profile.pid,
            role_title=role_title,
            organization=organization,
            start_year=int(start_year) if start_year else None,
            end_year=int(end_year) if end_year else None,
            description=description,
            sort_order=next_sort
        )
        db.session.add(er)
        db.session.commit()

        return jsonify({
            "success": True,
            "erid": er.erid,
            "role_title": er.role_title,
            "organization": er.organization,
            "start_year": er.start_year,
            "end_year": er.end_year,
            "description": er.description
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500


@main.route("/delete_external_role/<int:erid>", methods=["DELETE"])
@login_required
def delete_external_role(erid):
    if not validate_csrf_token():
        return jsonify({'success': False, 'error': 'Invalid CSRF token'}), 400
    
    try:
        profile = Profile.query.filter_by(user_id=current_user.id).first()
        if not profile:
            return jsonify({"success": False, "error": "Profile not found"}), 404

        er = ExternalRole.query.filter_by(erid=erid, pid=profile.pid).first()
        if not er:
            return jsonify({"success": False, "error": "External role not found"}), 404

        db.session.delete(er)
        db.session.commit()
        return jsonify({"success": True})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500


@main.route("/update_external_role_order", methods=["POST"])
@login_required
def update_external_role_order():
    if not validate_csrf_token():
        return jsonify({'success': False, 'error': 'Invalid CSRF token'}), 400
    
    try:
        data = request.get_json()
        order = data.get("order", [])
        if not isinstance(order, list):
            return jsonify({"success": False, "error": "Invalid order"}), 400

        profile = Profile.query.filter_by(user_id=current_user.id).first()
        if not profile:
            return jsonify({"success": False, "error": "Profile not found"}), 404

        # Assign sort_order based on incoming order list of erids
        for index, erid in enumerate(order, start=1):
            er = ExternalRole.query.filter_by(erid=int(erid), pid=profile.pid).first()
            if er:
                er.sort_order = index
        db.session.commit()
        return jsonify({"success": True})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500
    
@main.route("/add_achievement", methods=["POST"])
@login_required
def add_achievement():
    if not validate_csrf_token():
        return jsonify({'success': False, 'error': 'Invalid CSRF token'}), 400
    
    try:
        data = request.get_json()
        title = data.get("title", "").strip()
        achievement_type = data.get("type", "").strip()
        year = data.get("year")
        description = data.get("description", "").strip()

        if not title or not achievement_type:
            return jsonify({"success": False, "error": "title and type are required"}), 400

        profile = Profile.query.filter_by(user_id=current_user.id).first()
        if not profile:
            profile = Profile(user_id=current_user.id)
            db.session.add(profile)
            db.session.flush()

        # Determine next sort order
        max_sort = db.session.query(db.func.max(Achievement.aid)).filter_by(pid=profile.pid).scalar()

        ach = Achievement(
            pid=profile.pid,
            title=title,
            type=achievement_type,
            year=int(year) if year else None,
            description=description
        )
        db.session.add(ach)
        db.session.commit()

        return jsonify({
            "success": True,
            "aid": ach.aid,
            "title": ach.title,
            "type": ach.type,
            "year": ach.year,
            "description": ach.description
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500

@main.route("/delete_achievement/<int:aid>", methods=["DELETE"])
@login_required
def delete_achievement(aid):
    if not validate_csrf_token():
        return jsonify({'success': False, 'error': 'Invalid CSRF token'}), 400
    
    try:
        profile = Profile.query.filter_by(user_id=current_user.id).first()
        if not profile:
            return jsonify({"success": False, "error": "Profile not found"}), 404

        ach = Achievement.query.filter_by(aid=aid, pid=profile.pid).first()
        if not ach:
            return jsonify({"success": False, "error": "Achievement not found"}), 404

        db.session.delete(ach)
        db.session.commit()
        return jsonify({"success": True})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500
    
@main.route("/update_achievement_order", methods=["POST"])
@login_required
def update_achievement_order():
    if not validate_csrf_token():
        return jsonify({'success': False, 'error': 'Invalid CSRF token'}), 400
    
    try:
        data = request.get_json()
        order = data.get("order", [])
        if not isinstance(order, list):
            return jsonify({"success": False, "error": "Invalid order"}), 400

        profile = Profile.query.filter_by(user_id=current_user.id).first()
        if not profile:
            return jsonify({"success": False, "error": "Profile not found"}), 404

        # Assign sort_order based on incoming order list of aids
        for index, aid in enumerate(order, start=1):
            ach = Achievement.query.filter_by(aid=int(aid), pid=profile.pid).first()
            if ach:
                ach.sort_order = index
        db.session.commit()
        return jsonify({"success": True})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500