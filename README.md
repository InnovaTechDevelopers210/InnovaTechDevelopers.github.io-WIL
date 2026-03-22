# WIL Management System

A comprehensive web-based Internship & Placement (WIL) Management System built with Flask and Bootstrap.

## Project Information

- **Project Title:** Internship & Placement (WIL) Management System
- **Groups:** Group 15 & Group 22
- **Development Methodology:** Crystal (Yellow) Agile

## Features

### For Students
- Create and manage student profiles
- Browse and search internship opportunities
- Apply for internships with cover letters
- Track application status in real-time
- Upload and manage CV documents
- Receive notifications for application updates

### For Companies
- Create and manage company profiles
- Post internship opportunities
- Review and manage applications
- Schedule interviews
- Track placement progress

### For Administrators
- Manage users (students, companies, admins)
- Monitor all internships and applications
- Generate reports and statistics
- Verify company accounts
- View audit logs

## Technology Stack

### Frontend
- HTML5
- CSS3
- JavaScript
- Bootstrap 5
- Bootstrap Icons

### Backend
- Python 3.8+
- Flask 3.0
- SQLite (development) / PostgreSQL (production)

### Security
- bcrypt for password hashing
- CSRF protection
- Session management
- POPIA compliant

## Project Structure

```
wil-system/
├── app.py                  # Main application entry point
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables template
├── README.md               # This file
│
├── models/                 # Database models
│   ├── __init__.py
│   ├── user.py            # User authentication model
│   ├── student.py         # Student profile model
│   ├── company.py         # Company profile model
│   ├── internship.py      # Internship listing model
│   ├── application.py     # Application model
│   └── notification.py    # Notification model
│
├── routes/                 # Flask blueprints
│   ├── __init__.py
│   ├── auth_routes.py     # Authentication routes
│   ├── student_routes.py  # Student dashboard routes
│   ├── company_routes.py  # Company management routes
│   ├── admin_routes.py    # Admin panel routes
│   └── api_routes.py      # RESTful API routes
│
├── templates/              # HTML templates
│   ├── base.html          # Base template
│   ├── index.html         # Home page
│   ├── about.html         # About page
│   ├── privacy.html       # Privacy policy
│   ├── auth/              # Authentication templates
│   ├── student/           # Student templates
│   ├── company/           # Company templates
│   ├── admin/             # Admin templates
│   └── errors/            # Error page templates
│
├── static/                 # Static assets
│   ├── css/               # Stylesheets
│   ├── js/                # JavaScript files
│   └── uploads/           # User uploads (CVs, logos)
│
└── database/               # Database files
    └── schema.sql          # Database schema
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd wil-system
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` file with your configuration:

```env
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///database/wil_system.db
```

### Step 5: Initialize Database

The database will be automatically initialized when you first run the application.

### Step 6: Run the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Demo Accounts

The system comes with pre-configured demo accounts:

| Role    | Email                        | Password    |
|---------|------------------------------|-------------|
| Admin   | admin@wil-system.ac.za       | Admin@123   |
| Student | john.doe@student.edu         | Student@123 |
| Company | hr@techcorp.co.za            | Company@123 |

## Deployment

### Deploy to Render (Recommended)

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Configure environment variables in Render Dashboard
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `gunicorn app:app`

### Deploy to PythonAnywhere

1. Upload files to PythonAnywhere
2. Create a new web app with Flask
3. Update WSGI configuration
4. Set environment variables
5. Reload the web app

### Deploy to Heroku

```bash
# Install Heroku CLI and login
heroku login

# Create new Heroku app
heroku create your-app-name

# Add PostgreSQL addon
heroku addons:create heroku-postgresql:hobby-dev

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set FLASK_ENV=production

# Deploy
git push heroku main
```

## API Documentation

### Authentication
All API endpoints (except public ones) require authentication via session.

### Endpoints

#### Users
- `GET /api/user/me` - Get current user info
- `GET /api/user/<id>` - Get user by ID (admin only)

#### Internships
- `GET /api/internships` - List all active internships
- `GET /api/internship/<id>` - Get internship details
- `GET /api/internships/recent` - Get recent internships
- `GET /api/internships/closing-soon` - Get internships closing soon

#### Applications
- `GET /api/applications` - Get user's applications
- `GET /api/application/<id>` - Get application details
- `PUT /api/application/<id>/status` - Update application status

#### Notifications
- `GET /api/notifications` - Get user notifications
- `POST /api/notifications/<id>/read` - Mark notification as read
- `POST /api/notifications/read-all` - Mark all as read

#### Statistics
- `GET /api/statistics` - Get system statistics
- `GET /api/statistics/placements` - Get placement statistics

## Security Features

- **Password Security:** bcrypt hashing with salt
- **CSRF Protection:** All forms include CSRF tokens
- **Session Security:** Secure, HTTP-only cookies
- **Input Validation:** Server-side validation on all inputs
- **SQL Injection Prevention:** Parameterized queries
- **XSS Prevention:** Output escaping in templates
- **POPIA Compliance:** Data protection and privacy controls

## Development

### Running Tests

```bash
pytest
```

### Code Style

```bash
# Format with black
black .

# Lint with flake8
flake8 .
```

### Database Migrations

For production with PostgreSQL, use Flask-Migrate:

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Environment mode | `development` |
| `SECRET_KEY` | Flask secret key | Required |
| `DATABASE_URL` | Database connection URL | SQLite |
| `MAIL_SERVER` | SMTP server | `smtp.gmail.com` |
| `MAIL_PORT` | SMTP port | `587` |
| `MAIL_USERNAME` | Email username | None |
| `MAIL_PASSWORD` | Email password | None |

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Support

For support, email support@wil-system.ac.za or create an issue in the repository.

## Acknowledgments

- Group 15 & Group 22 for collaborative development
- Crystal (Yellow) Agile Methodology for project management
- Flask community for the excellent framework