<div align="center">
<img src="https://www.google.com/search?q=https://storage.googleapis.com/gemini-prod-us-west1-assets/v1/static/og-img-2.png" alt="AuraEventz Logo" width="150"/>
<h1>AuraEventz</h1>
<p><strong>The Ultimate Platform for Connecting Event Managers with a Skilled Workforce.</strong></p>
<p>Streamline your event staffing from start to finish. Post jobs, manage applicants, and find your next gig—all in one place.</p>

<!-- Badges -->

<p>
<img src="https://www.google.com/search?q=https://img.shields.io/badge/Python-3776AB%3Fstyle%3Dfor-the-badge%26logo%3Dpython%26logoColor%3Dwhite" alt="Python Badge"/>
<img src="https://www.google.com/search?q=https://img.shields.io/badge/Flask-000000%3Fstyle%3Dfor-the-badge%26logo%3Dflask%26logoColor%3Dwhite" alt="Flask Badge"/>
<img src="https://www.google.com/search?q=https://img.shields.io/badge/Firebase-FFCA28%3Fstyle%3Dfor-the-badge%26logo%3Dfirebase%26logoColor%3Dblack" alt="Firebase Badge"/>
<img src="https://www.google.com/search?q=https://img.shields.io/badge/Tailwind_CSS-38B2AC%3Fstyle%3Dfor-the-badge%26logo%3Dtailwind-css%26logoColor%3Dwhite" alt="Tailwind CSS Badge"/>
</p>
</div>

✨ Key Features
AuraEventz provides a seamless two-sided marketplace for the event industry:

For Event Managers:

👤 Role-Based Authentication: Secure registration and login for managers.

📋 Full CRUD for Jobs: Create, Read, Update, and Delete job postings with ease.

📊 Dashboard & Analytics: Get a quick overview of your posted jobs and the number of applicants.

✅ Applicant Management: View a list of all applicants for a specific job and Approve or Reject them with a single click.

For Event Workers:

👤 Secure Worker Accounts: Separate, secure registration and login for the workforce.

🔍 Browse & Apply: View all available jobs posted by managers and apply instantly.

📈 Track Application Status: A dedicated dashboard to see the real-time status (Pending, Approved, Rejected) of all your applications.

🚀 Find Opportunities: A clean and modern interface to find your next event gig.

🚀 Live Demo
Check out the live version of the application hosted on Render!

➡️ Visit AuraEventz Live (Replace with your actual Render URL)

🛠️ Technology Stack
Technology

Purpose

Python & Flask

Backend framework for routing, logic, and server-side rendering.

Firebase

Handles user authentication (Auth) and the database (Firestore).

HTML5 & Jinja2

Frontend structure and templating engine.

Tailwind CSS

Modern, utility-first CSS for a beautiful and responsive UI.

Gunicorn

Production-grade web server for running the Flask app.

Render

Cloud platform for hosting and automatic deployments.

🏁 Getting Started & Local Setup
Want to run this project on your local machine? Follow these steps.

Prerequisites
Python 3.8+

A Firebase project with Authentication and Firestore enabled.

Git

1. Clone the Repository
git clone [https://github.com/your-username/AuraEventz.git](https://github.com/your-username/AuraEventz.git)
cd AuraEventz

2. Set Up a Virtual Environment
It's highly recommended to use a virtual environment to keep dependencies isolated.

# For Windows
python -m venv venv
.\venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

3. Install Dependencies
pip install -r requirements.txt

4. Configure Environment Variables
Create a file named .env in the root of your project. This file holds your secret keys and is ignored by Git. Copy the contents of your Firebase project's configuration here.

.env file structure:

# A secret key for Flask sessions
SECRET_KEY='a_very_long_random_string_here'

# Firebase Admin SDK Credentials (as a single JSON string)
FIREBASE_JSON_CONTENT='{"type": "service_account", "project_id": "...", ...}'

# Firebase Client SDK Credentials (for the frontend)
FIREBASE_API_KEY="AIzaSy..."
FIREBASE_AUTH_DOMAIN="your-project.firebaseapp.com"
FIREBASE_PROJECT_ID="your-project-id"

How to get FIREBASE_JSON_CONTENT:

In your Firebase project, go to Project Settings > Service accounts.

Click "Generate new private key".

Open the downloaded JSON file, copy the entire content, and paste it as a single line for the FIREBASE_JSON_CONTENT value.

5. Run the Application
flask run
