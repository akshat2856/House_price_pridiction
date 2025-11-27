# Authentication System Documentation

## Overview
This document describes the complete authentication system implemented in the Delhi House Finder application using Flask-Login and Flask-SQLAlchemy.

## Technology Stack
- **Flask-Login**: Session management and user authentication
- **Flask-SQLAlchemy**: ORM for database operations
- **SQLite**: Lightweight database for user storage
- **Werkzeug Security**: Password hashing with PBKDF2-SHA256

## Database Schema

### User Model (`database.py`)
```python
class User(UserMixin, db.Model):
    id              # Primary key (Integer)
    email           # Unique, required (String 150)
    password_hash   # Hashed password (String 200)
    full_name       # User's full name (String 150)
    role            # 'buyer' or 'seller' (String 20)
    created_at      # Timestamp (DateTime)
```

**Key Methods:**
- `set_password(password)`: Hashes and stores password
- `check_password(password)`: Verifies password against hash
- `to_dict()`: Returns user data as dictionary (excludes password)

## Authentication Routes

### 1. Sign Up (`/signup`)
**Method**: GET, POST  
**Access**: Public

**Features:**
- Email validation (unique constraint)
- Password confirmation matching
- Role selection (buyer/seller)
- Password hashing with Werkzeug
- Automatic redirect to sign-in after registration

**Form Fields:**
- Email (required, unique)
- Password (required, min 6 characters)
- Confirm Password (required, must match)
- Full Name (required)
- Role (radio: buyer/seller)

### 2. Sign In (`/signin`)
**Method**: GET, POST  
**Access**: Public

**Features:**
- Email and password authentication
- Remember me functionality (cookie persistence)
- Flash messages for errors
- Redirect to dashboard on success
- Redirect to original page if trying to access protected route

**Security:**
- Password verification with `check_password()`
- Session management via Flask-Login
- Protected against timing attacks

### 3. Logout (`/logout`)
**Method**: GET  
**Access**: Authenticated users only

**Features:**
- Clears user session
- Redirects to sign-in page
- Flash message confirmation

## Protected Routes
All main application routes are protected with `@login_required`:
- `/dashboard` - Browse properties
- `/price-prediction` - ML price prediction
- `/emi-calculator` - EMI calculations
- `/map-view` - Interactive heatmap
- All API endpoints (`/api/*`)

## User Interface

### Navigation Bar
**Authenticated State:**
```html
<user-icon> Full Name (role) <logout-icon>
```

**Unauthenticated State:**
```html
[Sign In] [Sign Up]
```

### Sign Up Page
- Modern gradient design
- Role selection cards with icons:
  - 🛒 Buyer: Find your dream home
  - 🏪 Seller: List and sell properties
- Client-side password validation
- Flash message support

### Sign In Page
- Clean, professional design
- Remember me checkbox
- Link to sign up page
- Flash message support

## Demo Accounts

### Buyer Account
- **Email**: demo@delhihouse.com
- **Password**: demo123
- **Role**: buyer

### Seller Account
- **Email**: seller@delhihouse.com
- **Password**: seller123
- **Role**: seller

## Database Initialization

The database is automatically initialized on first run:
1. Creates `users.db` SQLite database
2. Creates User table with schema
3. Seeds demo accounts (if not exist)

**Location**: `d:\Sach_me_mini_project\users.db`

**Manual Reset** (if needed):
```bash
# Delete the database file
rm users.db

# Restart the application - it will recreate everything
python app.py
```

## Security Features

### Password Security
- **Hashing Algorithm**: PBKDF2-SHA256 (Werkzeug default)
- **Salt**: Automatically generated per user
- **Iterations**: 260,000+ (Werkzeug default)
- **Password Requirements**: Minimum 6 characters (frontend validation)

### Session Security
- **Secret Key**: Configured in `app.secret_key`
- **Cookie Settings**: 
  - `SESSION_COOKIE_SAMESITE = 'Lax'`
  - `SESSION_COOKIE_SECURE = False` (set to True in production with HTTPS)
- **Login Message**: Custom flash message on unauthorized access

### Protection Against
- ✅ SQL Injection (SQLAlchemy parameterization)
- ✅ Password Rainbow Tables (salted hashing)
- ✅ Session Fixation (Flask-Login session regeneration)
- ✅ CSRF (Flask built-in protection)

## Usage Examples

### Accessing Current User in Routes
```python
@app.route('/profile')
@login_required
def profile():
    user_email = current_user.email
    user_role = current_user.role
    return render_template('profile.html', user=current_user)
```

### Accessing Current User in Templates
```html
{% if current_user.is_authenticated %}
    <p>Welcome, {{ current_user.full_name }}!</p>
    <p>Role: {{ current_user.role }}</p>
{% else %}
    <a href="{{ url_for('signin') }}">Sign In</a>
{% endif %}
```

### Creating New Users Programmatically
```python
new_user = User(
    email='user@example.com',
    full_name='John Doe',
    role='buyer'
)
new_user.set_password('secure_password')
db.session.add(new_user)
db.session.commit()
```

## Future Enhancements

### Recommended Improvements
1. **Email Verification**: Send confirmation emails on signup
2. **Password Reset**: Forgot password functionality
3. **OAuth Integration**: Google/Facebook login
4. **Role-Based Features**: 
   - Buyers: Save favorites, property alerts
   - Sellers: List properties, analytics dashboard
5. **Two-Factor Authentication**: SMS/TOTP for extra security
6. **Password Strength Meter**: Real-time feedback
7. **Account Management**: Edit profile, change password
8. **Admin Panel**: User management interface

## Troubleshooting

### Issue: "User not found" error
**Solution**: Check if database exists and has users table
```bash
python -c "from app import app, db; from database import User; app.app_context().push(); print(User.query.all())"
```

### Issue: Password not matching
**Solution**: Verify password is being hashed correctly
- Check `set_password()` is called before saving
- Ensure `check_password()` is used for verification

### Issue: Redirects to signin on every page
**Solution**: Check session configuration
- Verify `app.secret_key` is set
- Check cookie settings in browser
- Ensure Flask-Login is initialized correctly

## Files Modified

### New Files
- `database.py` - User model and database configuration
- `templates/signup.html` - Registration page
- `templates/signin.html` - Login page
- `AUTHENTICATION_SETUP.md` - This documentation

### Modified Files
- `app.py` - Added authentication routes and Flask-Login integration
- `templates/dashboard.html` - Updated navbar with auth buttons
- `templates/price_prediction.html` - Updated navbar with auth buttons
- `templates/emi_calculator.html` - Updated navbar with auth buttons
- `templates/map_view.html` - Updated navbar with auth buttons
- `static/css/style.css` - Added auth button styles
- `requirements.txt` - Added Flask-Login and Flask-SQLAlchemy

## Testing Checklist

- [x] Database tables created successfully
- [x] Demo accounts seeded
- [x] Sign up creates new user
- [x] Sign in with correct credentials
- [x] Sign in with wrong password fails
- [x] Protected routes redirect to sign-in
- [x] Logout clears session
- [x] Remember me persists session
- [x] Navbar shows user info when authenticated
- [x] Navbar shows sign-in/sign-up when not authenticated
- [x] Role displayed correctly (buyer/seller)

## Production Deployment Notes

Before deploying to production:

1. **Change Secret Key**:
   ```python
   app.secret_key = os.environ.get('SECRET_KEY') or 'your-very-secure-random-key'
   ```

2. **Enable HTTPS Cookie Security**:
   ```python
   app.config['SESSION_COOKIE_SECURE'] = True
   ```

3. **Use Production Database**:
   - Replace SQLite with PostgreSQL/MySQL
   - Update `SQLALCHEMY_DATABASE_URI`

4. **Add Password Requirements**:
   - Minimum 8 characters
   - Require uppercase, lowercase, number, special char

5. **Enable Rate Limiting**:
   - Install `flask-limiter`
   - Limit login attempts to prevent brute force

6. **Add Logging**:
   - Log authentication events
   - Monitor failed login attempts

7. **Use Production WSGI Server**:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:8000 app:app
   ```

---

**Last Updated**: January 2025  
**Version**: 1.0  
**Maintainer**: Delhi House Finder Team
