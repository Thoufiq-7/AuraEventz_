import os
import json
from flask import Flask, render_template, redirect, url_for, request, session, flash
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, auth, firestore
from datetime import datetime

# Load environment variables from .env file
load_dotenv() 

# Initialize Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = os.environ.get('SECRET_KEY', 'default_secret_for_dev')

# --- Firebase Admin SDK Initialization (Server-Side) ---
try:
    firebase_json_content = os.environ.get("FIREBASE_JSON_CONTENT")
    if firebase_json_content:
        cred_dict = json.loads(firebase_json_content)
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)
        print("Firebase Admin SDK initialized successfully using environment JSON.")
    else:
        # Fallback for environments like Google Cloud Platform
        firebase_admin.initialize_app()
        print("FIREBASE_JSON_CONTENT not found. Attempting Application Default Credentials.")
    
    # Initialize Firestore client
    db = firestore.client()
    print("Firestore client initialized.")
except Exception as e:
    print(f"FATAL: Error initializing Firebase: {e}")
    db = None # Set db to None if initialization fails

# --- Helper Functions ---

def get_client_firebase_config():
    """
    Returns the necessary config for the Firebase Client SDK (JS).
    Includes print statements for debugging on Render.
    """
    config = {
        "apiKey": os.environ.get("FIREBASE_API_KEY"),
        "authDomain": os.environ.get("FIREBASE_AUTH_DOMAIN"),
        "projectId": os.environ.get("FIREBASE_PROJECT_ID"),
    }
    
    # --- DEBUG PRINTS ---
    # These will show up in your Render logs
    print("--- DEBUGGING FIREBASE CLIENT CONFIG ---")
    print(f"API Key is present: {config['apiKey'] is not None}")
    print(f"Auth Domain is present: {config['authDomain'] is not None}")
    print(f"Project ID is present: {config['projectId'] is not None}")
    print(f"Final config object being sent to template: {config}")
    print("--- END DEBUGGING ---")
    
    return config

def login_required(required_role=None):
    """Checks if the user is logged in and has the required role."""
    user_id = session.get('user_id')
    user_role = session.get('user_role')
    if not user_id:
        flash('Please log in to access this page.', 'info')
        return False, 'index'
    if required_role and user_role != required_role:
        flash(f'Access denied. This page is for {required_role}s only.', 'danger')
        # Redirect to the correct dashboard if they are logged in with the wrong role
        if user_role == 'manager':
             return False, 'manager_dashboard'
        elif user_role == 'worker':
             return False, 'worker_dashboard'
    return True, None

# --- Main Routes ---

@app.route('/')
def index():
    """Renders the main landing page."""
    return render_template('index.html')

@app.route('/logout')
def logout():
    """Logs out the current user."""
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

# --- Manager Routes ---

@app.route('/manager/login-register')
def manager_login_register():
    config = get_client_firebase_config()
    return render_template('manager_login_register.html', firebase_config=config)

@app.route('/manager/register', methods=['POST'])
def manager_register():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    if not all([username, email, password]):
        flash('Please fill out all fields.', 'danger')
        return redirect(url_for('manager_login_register'))
    try:
        user = auth.create_user(email=email, password=password, display_name=username)
        auth.set_custom_user_claims(user.uid, {'role': 'manager'})
        flash('Registration successful! Please sign in.', 'success')
    except Exception as e:
        flash(f'Registration failed: {e}', 'danger')
    return redirect(url_for('manager_login_register'))

@app.route('/manager/login', methods=['POST'])
def manager_login():
    id_token = request.form.get('id_token')
    if not id_token:
        flash('Authentication token missing.', 'danger')
        return redirect(url_for('manager_login_register'))
    try:
        claims = auth.verify_id_token(id_token)
        if claims.get('role') != 'manager':
            flash('Access denied. This is not a Manager account.', 'danger')
            return redirect(url_for('manager_login_register'))
        session['user_id'] = claims['uid']
        session['user_role'] = 'manager'
        flash('Logged in successfully!', 'success')
        return redirect(url_for('manager_dashboard'))
    except Exception as e:
        flash(f'Authentication failed: {e}', 'danger')
        return redirect(url_for('manager_login_register'))

@app.route('/manager/dashboard')
def manager_dashboard():
    is_auth, redirect_route = login_required('manager')
    if not is_auth:
        return redirect(url_for(redirect_route))
    
    if not db:
        flash("Database connection is not available.", "danger")
        return render_template('manager_dashboard.html', jobs=[])

    jobs = []
    try:
        user_id = session.get('user_id')
        jobs_ref = db.collection('jobs').where('posted_by', '==', user_id).stream()
        for job in jobs_ref:
            job_data = job.to_dict()
            job_data['id'] = job.id
            apps_query = db.collection('applications').where('job_id', '==', job.id).stream()
            job_data['app_count'] = len(list(apps_query))
            jobs.append(job_data)
    except Exception as e:
        flash(f"Error fetching jobs: {e}", "danger")

    return render_template('manager_dashboard.html', jobs=jobs)

@app.route('/manager/post-job', methods=['GET', 'POST'])
def manager_post_job():
    is_auth, redirect_route = login_required('manager')
    if not is_auth:
        return redirect(url_for(redirect_route))
    
    if request.method == 'POST':
        if not db:
            flash("Database not available.", "danger")
            return redirect(url_for('manager_dashboard'))
        try:
            job_data = {
                'title': request.form.get('title'),
                'location': request.form.get('location'),
                'description': request.form.get('description'),
                'salary': request.form.get('salary', 'N/A'),
                'posted_by': session.get('user_id'),
                'posted_on': datetime.utcnow().strftime('%b %d, %Y'),
                'status': 'Active'
            }
            db.collection('jobs').add(job_data)
            flash('Job posted successfully!', 'success')
            return redirect(url_for('manager_dashboard'))
        except Exception as e:
            flash(f"Error posting job: {e}", "danger")
            return redirect(url_for('manager_post_job'))

    return render_template('post_job.html')

@app.route('/manager/edit-job/<job_id>')
def edit_job(job_id):
    is_auth, redirect_route = login_required('manager')
    if not is_auth: return redirect(url_for(redirect_route))
    if not db:
        flash("Database not available.", "danger")
        return redirect(url_for('manager_dashboard'))

    try:
        job_ref = db.collection('jobs').document(job_id).get()
        if not job_ref.exists:
            flash("Job not found.", "danger")
            return redirect(url_for('manager_dashboard'))
        
        job_data = job_ref.to_dict()
        if job_data.get('posted_by') != session.get('user_id'):
            flash("You do not have permission to edit this job.", "danger")
            return redirect(url_for('manager_dashboard'))

        return render_template('edit_job.html', job=job_data, job_id=job_id)
    except Exception as e:
        flash(f"Error fetching job for edit: {e}", "danger")
        return redirect(url_for('manager_dashboard'))

@app.route('/manager/update-job/<job_id>', methods=['POST'])
def update_job(job_id):
    is_auth, redirect_route = login_required('manager')
    if not is_auth: return redirect(url_for(redirect_route))
    if not db:
        flash("Database not available.", "danger")
        return redirect(url_for('manager_dashboard'))
    
    try:
        # Security check: Ensure manager owns the job before updating
        job_ref = db.collection('jobs').document(job_id).get()
        if not job_ref.exists or job_ref.to_dict().get('posted_by') != session.get('user_id'):
            flash("You do not have permission to update this job.", "danger")
            return redirect(url_for('manager_dashboard'))
        
        updated_data = {
            'title': request.form.get('title'),
            'location': request.form.get('location'),
            'description': request.form.get('description'),
            'salary': request.form.get('salary')
        }
        db.collection('jobs').document(job_id).update(updated_data)
        flash("Job updated successfully!", "success")
    except Exception as e:
        flash(f"Error updating job: {e}", "danger")
    
    return redirect(url_for('manager_dashboard'))

@app.route('/manager/delete-job/<job_id>', methods=['POST'])
def delete_job(job_id):
    is_auth, redirect_route = login_required('manager')
    if not is_auth: return redirect(url_for(redirect_route))
    if not db:
        flash("Database not available.", "danger")
        return redirect(url_for('manager_dashboard'))
    
    try:
        job_ref = db.collection('jobs').document(job_id)
        job_doc = job_ref.get()

        if job_doc.exists and job_doc.to_dict().get('posted_by') == session.get('user_id'):
            # Cascading Delete: Delete all applications for this job first
            apps_query = db.collection('applications').where('job_id', '==', job_id).stream()
            for app in apps_query:
                app.reference.delete()
            
            # Now delete the job itself
            job_ref.delete()
            flash("Job and all its applications have been deleted.", "success")
        else:
            flash("Job not found or you don't have permission to delete it.", "danger")
    except Exception as e:
        flash(f"Error deleting job: {e}", "danger")
        
    return redirect(url_for('manager_dashboard'))

@app.route('/manager/job/<job_id>/applicants')
def view_applicants(job_id):
    is_auth, redirect_route = login_required('manager')
    if not is_auth: return redirect(url_for(redirect_route))
    if not db:
        flash("Database not available.", "danger")
        return redirect(url_for('manager_dashboard'))
    
    try:
        job_ref = db.collection('jobs').document(job_id).get()
        if not job_ref.exists or job_ref.to_dict().get('posted_by') != session.get('user_id'):
            flash("Job not found or you don't have permission.", "danger")
            return redirect(url_for('manager_dashboard'))
        
        job_title = job_ref.to_dict().get('title', 'Job')
        applications = [doc.to_dict() | {'id': doc.id} for doc in db.collection('applications').where('job_id', '==', job_id).stream()]
        
        return render_template('view_applicants.html', applications=applications, job_title=job_title)
    except Exception as e:
        flash(f"Error fetching applicants: {e}", "danger")
        return redirect(url_for('manager_dashboard'))

@app.route('/manager/update-application-status/<app_id>', methods=['POST'])
def update_application_status(app_id):
    is_auth, redirect_route = login_required('manager')
    if not is_auth: return redirect(url_for(redirect_route))
    if not db:
        flash("Database not available.", "danger")
        return redirect(url_for('manager_dashboard'))

    try:
        new_status = request.form.get('status')
        app_ref = db.collection('applications').document(app_id)
        job_id = app_ref.get().to_dict().get('job_id')
        
        # Security check here is a good idea
        
        app_ref.update({'status': new_status})
        flash(f"Application status updated to {new_status}.", "success")
        return redirect(url_for('view_applicants', job_id=job_id))
    except Exception as e:
        flash(f"Error updating status: {e}", "danger")
        return redirect(url_for('manager_dashboard'))

# --- Worker Routes ---

@app.route('/worker/login-register')
def worker_login_register():
    config = get_client_firebase_config()
    return render_template('worker_login_register.html', firebase_config=config)

@app.route('/worker/register', methods=['POST'])
def worker_register():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    if not all([username, email, password]):
        flash('Please fill out all fields.', 'danger')
        return redirect(url_for('worker_login_register'))
    try:
        user = auth.create_user(email=email, password=password, display_name=username)
        auth.set_custom_user_claims(user.uid, {'role': 'worker'})
        flash('Registration successful! Please sign in.', 'success')
    except Exception as e:
        flash(f'Registration failed: {e}', 'danger')
    return redirect(url_for('worker_login_register'))

@app.route('/worker/login', methods=['POST'])
def worker_login():
    id_token = request.form.get('id_token')
    if not id_token:
        flash('Authentication token missing.', 'danger')
        return redirect(url_for('worker_login_register'))
    try:
        claims = auth.verify_id_token(id_token)
        if claims.get('role') != 'worker':
            flash('Access denied. This is not a Worker account.', 'danger')
            return redirect(url_for('worker_login_register'))
        session['user_id'] = claims['uid']
        session['user_role'] = 'worker'
        flash('Logged in successfully!', 'success')
        return redirect(url_for('worker_dashboard'))
    except Exception as e:
        flash(f'Authentication failed: {e}', 'danger')
        return redirect(url_for('worker_login_register'))

@app.route('/worker/dashboard')
def worker_dashboard():
    is_auth, redirect_route = login_required('worker')
    if not is_auth: return redirect(url_for(redirect_route))
    if not db:
        flash("Database not available.", "danger")
        return render_template('worker_dashboard.html', job_count=0, application_count=0)
        
    job_count = len(list(db.collection('jobs').where('status', '==', 'Active').stream()))
    application_count = len(list(db.collection('applications').where('worker_id', '==', session['user_id']).stream()))

    return render_template('worker_dashboard.html', job_count=job_count, application_count=application_count)

@app.route('/worker/jobs')
def worker_jobs():
    is_auth, redirect_route = login_required('worker')
    if not is_auth: return redirect(url_for(redirect_route))
    if not db:
        flash("Database not available.", "danger")
        return render_template('worker_jobs.html', jobs=[], applied_job_ids=set())
        
    try:
        jobs_ref = db.collection('jobs').where('status', '==', 'Active').stream()
        jobs = [doc.to_dict() | {'id': doc.id} for doc in jobs_ref]

        apps_ref = db.collection('applications').where('worker_id', '==', session['user_id']).stream()
        applied_job_ids = {app.to_dict()['job_id'] for app in apps_ref}
        
        return render_template('worker_jobs.html', jobs=jobs, applied_job_ids=applied_job_ids)
    except Exception as e:
        flash(f"Error fetching jobs: {e}", "danger")
        return render_template('worker_jobs.html', jobs=[], applied_job_ids=set())

@app.route('/worker/apply-job/<job_id>', methods=['POST'])
def apply_job(job_id):
    is_auth, redirect_route = login_required('worker')
    if not is_auth: return redirect(url_for(redirect_route))
    if not db:
        flash("Database not available.", "danger")
        return redirect(url_for('worker_jobs'))

    try:
        worker_id = session['user_id']
        
        existing_app_query = db.collection('applications').where('worker_id', '==', worker_id).where('job_id', '==', job_id).limit(1).stream()
        if len(list(existing_app_query)) > 0:
            flash("You have already applied for this job.", "info")
            return redirect(url_for('worker_jobs'))

        job_ref = db.collection('jobs').document(job_id).get()
        if not job_ref.exists:
            flash("This job posting is no longer available.", "danger")
            return redirect(url_for('worker_jobs'))
        
        worker_user = auth.get_user(worker_id)
        job_data = job_ref.to_dict()

        application_data = {
            'job_id': job_id,
            'job_title': job_data.get('title'),
            'manager_id': job_data.get('posted_by'),
            'worker_id': worker_id,
            'worker_name': worker_user.display_name,
            'applied_on': datetime.utcnow().strftime('%b %d, %Y'),
            'status': 'Pending'
        }
        db.collection('applications').add(application_data)
        flash("Successfully applied for the job!", "success")
    except Exception as e:
        flash(f"Error submitting application: {e}", "danger")

    return redirect(url_for('worker_jobs'))

@app.route('/worker/my-applications')
def worker_my_applications():
    is_auth, redirect_route = login_required('worker')
    if not is_auth: return redirect(url_for(redirect_route))
    if not db:
        flash("Database not available.", "danger")
        return render_template('worker_my_applications.html', applications=[])
        
    try:
        apps_ref = db.collection('applications').where('worker_id', '==', session['user_id']).stream()
        applications = [app.to_dict() for app in apps_ref]
        return render_template('worker_my_applications.html', applications=applications)
    except Exception as e:
        flash(f"Error fetching your applications: {e}", "danger")
        return render_template('worker_my_applications.html', applications=[])

if __name__ == '__main__':
    app.run(debug=True)