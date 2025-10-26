# AuraEventz

**The Ultimate Platform for Connecting Event Managers with a Skilled Workforce.**

Streamline your event staffing from start to finish. Post jobs, manage applicants, and find your next gig—all in one place.

## 🚀 Live Demo

Check out the live version of the application hosted on Render!

**[Visit AuraEventz Live](# AuraEventz

**The Ultimate Platform for Connecting Event Managers with a Skilled Workforce.**

Streamline your event staffing from start to finish. Post jobs, manage applicants, and find your next gig—all in one place.

## 🚀 Live Demo

Check out the live version of the application hosted on Render!

**[Visit AuraEventz Live](https://auraeventz.onrender.com)** 

## ✨ Key Features

AuraEventz provides a seamless two-sided marketplace for the event industry.

### For Event Managers
* **Role-Based Authentication:** Secure registration and login for managers.
* **Full CRUD for Jobs:** Create, Read, Update, and Delete job postings with ease.
* **Dashboard & Analytics:** Get a quick overview of your posted jobs and the number of applicants.
* **Applicant Management:** View a list of all applicants for a specific job and Approve or Reject them with a single click.

### For Event Workers
* **Secure Worker Accounts:** Separate, secure registration and login for the workforce.
* **Browse & Apply:** View all available jobs posted by managers and apply instantly.
* **Track Application Status:** A dedicated dashboard to see the real-time status (Pending, Approved, Rejected) of all your applications.
* **Find Opportunities:** A clean and modern interface to find your next event gig.

## 🛠️ Technology Stack

| Technology | Purpose |
| :--- | :--- |
| Python & Flask | Backend framework for routing, logic, and server-side rendering. |
| Firebase | Handles user authentication (Auth) and the database (Firestore). |
| HTML5 & Jinja2 | Frontend structure and templating engine. |
| Tailwind CSS | Modern, utility-first CSS for a beautiful and responsive UI. |
| Gunicorn | Production-grade web server for running the Flask app. |
| Render | Cloud platform for hosting and automatic deployments. |

## 📂 Project Structure

A high-level overview of the project's directory to help you navigate the codebase.)** (Replace with your actual Render URL)

## ✨ Key Features

AuraEventz provides a seamless two-sided marketplace for the event industry.

### For Event Managers
* **Role-Based Authentication:** Secure registration and login for managers.
* **Full CRUD for Jobs:** Create, Read, Update, and Delete job postings with ease.
* **Dashboard & Analytics:** Get a quick overview of your posted jobs and the number of applicants.
* **Applicant Management:** View a list of all applicants for a specific job and Approve or Reject them with a single click.

### For Event Workers
* **Secure Worker Accounts:** Separate, secure registration and login for the workforce.
* **Browse & Apply:** View all available jobs posted by managers and apply instantly.
* **Track Application Status:** A dedicated dashboard to see the real-time status (Pending, Approved, Rejected) of all your applications.
* **Find Opportunities:** A clean and modern interface to find your next event gig.

## 🛠️ Technology Stack

| Technology | Purpose |
| :--- | :--- |
| Python & Flask | Backend framework for routing, logic, and server-side rendering. |
| Firebase | Handles user authentication (Auth) and the database (Firestore). |
| HTML5 & Jinja2 | Frontend structure and templating engine. |
| Tailwind CSS | Modern, utility-first CSS for a beautiful and responsive UI. |
| Gunicorn | Production-grade web server for running the Flask app. |
| Render | Cloud platform for hosting and automatic deployments. |

## 📂 Project Structure

A high-level overview of the project's directory to help you navigate the codebase.

AuraEventz/ 

├── app.py # Main Flask application (routes, auth, CRUD logic) 

├── requirements.txt # All Python dependencies 

├── .env # Environment variables (Firebase keys, Secret Key) 

├── firebase_config.py # Initialization logic for Firebase Admin SDK 

├── static/
 
 │ └── templates/ 
  
        ├── base.html # Main layout file (navbar, footer) 
    
        ├── index.html # Landing page 
    
        ├── auth/ # Login and register pages 
        
        ├── manager/ # Manager dashboard, create/edit event pages 
    
        └── worker/ # Worker dashboard, job list page

## 🏁 Getting Started & Local Setup

Want to run this project on your local machine? Follow these steps.

### Prerequisites
* Python 3.8+
* A Firebase project with **Authentication** and **Firestore** enabled.
* Git

### 1. Clone the Repository
```bash
git clone [https://github.com/your-username/AuraEventz.git](https://github.com/your-username/AuraEventz.git)
cd AuraEventz

2. Set Up a Virtual Environment

It's highly recommended to use a virtual environment to keep dependencies isolated.

For Windows:
python -m venv venv
.\venv\Scripts\activate

For macOS/Linux:

Bash

python3 -m venv venv
source venv/bin/activate

3. Install Dependencies
Bash

pip install -r requirements.txt

4. Configure Environment Variables
Create a file named .env in the root of your project. This file holds your secret keys and is ignored by Git.

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
Bash

flask run
