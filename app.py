"""
WIL Management System - Main Application
Flask Application Entry Point

This is the main application file that initializes the Flask app,
registers blueprints, and defines global routes.
"""

import os
import sqlite3
from datetime import datetime
from flask import Flask, render_template, g, session, request, jsonify

from config import config

# ============================================
# APPLICATION FACTORY
# ============================================

def create_app(config_name='development'):
    """Application factory pattern"""
    
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'cvs'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'logos'), exist_ok=True)
    os.makedirs(os.path.join(os.path.dirname(__file__), 'logs'), exist_ok=True)
    
    # Initialize database
    init_database(app)
    
    # Register blueprints
    register_blueprints(app)
    
    # Register context processors
    register_context_processors(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Register before/after request handlers
    register_request_handlers(app)
    
    # Register custom Jinja filters
    register_filters(app)
    
    return app

# ============================================
# DATABASE
# ============================================

def init_database(app):
    """Initialize database with schema"""
    db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
    
    if not os.path.exists(db_path):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        schema_path = os.path.join(os.path.dirname(__file__), 'database', 'schema.sql')
        if os.path.exists(schema_path):
            with sqlite3.connect(db_path) as conn:
                with open(schema_path, 'r') as f:
                    conn.executescript(f.read())
            print(f"Database initialized at {db_path}")

# ============================================
# BLUEPRINTS
# ============================================

def register_blueprints(app):
    """Register Flask blueprints"""
    from routes.auth_routes import auth_bp
    from routes.student_routes import student_bp
    from routes.company_routes import company_bp
    from routes.admin_routes import admin_bp
    from routes.api_routes import api_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(company_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp)

# ============================================
# CONTEXT PROCESSORS
# ============================================

def register_context_processors(app):
    """Register template context processors"""
    
    @app.context_processor
    def inject_now():
        return {'now': datetime.now}
    
    @app.context_processor
    def inject_csrf_token():
        """Inject CSRF token for forms"""
        return {'csrf_token': lambda: session.get('_csrf_token', '')}

# ============================================
# JINJA FILTERS
# ============================================

def register_filters(app):
    """Register custom Jinja filters"""
    
    @app.template_filter('safe_date')
    def safe_date(value, fmt='%Y-%m-%d'):
        """Safely format datetime objects, fallback to string or 'N/A'"""
        if isinstance(value, datetime):
            return value.strftime(fmt)
        elif isinstance(value, str):
            # Try parsing ISO string
            try:
                dt = datetime.fromisoformat(value)
                return dt.strftime(fmt)
            except ValueError:
                return value  # fallback: show string as-is
        return 'N/A'

# ============================================
# ERROR HANDLERS
# ============================================

def register_error_handlers(app):
    """Register error handlers"""
    
    @app.errorhandler(404)
    def not_found_error(error):
        if request.path.startswith('/api/'):
            return jsonify({'error': 'Resource not found'}), 404
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        if request.path.startswith('/api/'):
            return jsonify({'error': 'Internal server error'}), 500
        return render_template('errors/500.html'), 500
    
    @app.errorhandler(403)
    def forbidden_error(error):
        if request.path.startswith('/api/'):
            return jsonify({'error': 'Forbidden'}), 403
        return render_template('errors/403.html'), 403

# ============================================
# REQUEST HANDLERS
# ============================================

def register_request_handlers(app):
    """Register before/after request handlers"""
    
    @app.before_request
    def before_request():
        """Actions before each request"""
        if '_csrf_token' not in session:
            import secrets
            session['_csrf_token'] = secrets.token_hex(32)
    
    @app.teardown_appcontext
    def close_db(error):
        """Close database connection"""
        if hasattr(g, 'db'):
            g.db.close()

# ============================================
# MAIN ROUTES
# ============================================

def create_main_routes(app):
    """Create main application routes"""
    
    from models import Internship, User

    @app.route('/')
    def index():
        """Home page"""
        # --- Initialize variables so base.html doesn't break ---
        notifications = []
        unread_notifications = 0
        is_logged_in = False
        current_user_role = ''
        current_user_name = ''

        # --- Get featured internships ---
        featured = Internship.get_recent(limit=6)
        
        # --- Get statistics ---
        stats = {
            'total_students': User.count_all(role='student'),
            'total_companies': User.count_all(role='company'),
            'total_internships': Internship.count_all(),
            'placement_rate': 85  # Placeholder, calculate dynamically
        }
        
        return render_template('index.html', 
                               notifications=notifications,
                               unread_notifications=unread_notifications,
                               is_logged_in=is_logged_in,
                               current_user_role=current_user_role,
                               current_user_name=current_user_name,
                               featured_internships=featured,
                               **stats)
    
    @app.route('/about')
    def about():
        return render_template('about.html')
    
    @app.route('/privacy-policy')
    def privacy():
        return render_template('privacy.html')
    
    @app.route('/terms-of-service')
    def terms():
        return render_template('terms.html')
    
    @app.route('/contact')
    def contact():
        return render_template('contact.html')
    
    @app.route('/dashboard')
    def dashboard():
        """Redirect logged-in users to their dashboards"""
        if 'user_id' not in session:
            return render_template('index.html')
        
        role = session.get('user_role')
        
        from flask import redirect, url_for
        if role == 'admin':
            return redirect(url_for('admin.dashboard'))
        elif role == 'student':
            return redirect(url_for('student.dashboard'))
        elif role == 'company':
            return redirect(url_for('company.dashboard'))
        
        return render_template('index.html')

# ============================================
# CREATE APP INSTANCE
# ============================================

config_name = os.environ.get('FLASK_ENV', 'development')
app = create_app(config_name)
create_main_routes(app)

# ============================================
# CLI COMMANDS
# ============================================

@app.cli.command('init-db')
def init_db_command():
    init_database(app)
    print('Database initialized.')

@app.cli.command('create-admin')
def create_admin_command():
    from models import User
    with app.app_context():
        try:
            user = User.create(
                email='admin@wil-system.ac.za',
                password='Admin123',
                first_name='System',
                last_name='Administrator',
                role='admin',
                consent_given=True
            )
            print(f'Admin user created: {user.email}')
        except ValueError as e:
            print(f'Error: {e}')

# ============================================
# MAIN ENTRY POINT
# ============================================

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=config_name == 'development'
    )