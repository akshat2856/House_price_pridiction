# 🏠 Delhi House Finder - Complete Setup & User Guide

## ✨ What's New - Authentication System

This project now includes a complete authentication system with:
- ✅ User registration and login
- ✅ Secure password hashing
- ✅ Role-based accounts (buyer/seller)
- ✅ Session management
- ✅ Protected routes

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Install Dependencies
```bash
# Navigate to project
cd d:\Sach_me_mini_project

# Install all packages
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
python app.py
```

### Step 3: Open Browser
Go to: **http://localhost:5000**

### Step 4: Sign In
Use demo account:
- **Email**: demo@delhihouse.com
- **Password**: demo123

---

## 📧 Demo Accounts

| Account Type | Email | Password | Role |
|--------------|-------|----------|------|
| Buyer Demo | demo@delhihouse.com | demo123 | buyer |
| Seller Demo | seller@delhihouse.com | seller123 | seller |

**Or create your own account**: Click "Sign Up" on homepage

---

## 🎯 Complete Feature Tour

### 1️⃣ Authentication System (NEW!)

#### Sign Up
- Navigate to http://localhost:5000/signup
- Enter email, password, full name
- Choose role: Buyer or Seller
- Submit → Automatically redirects to sign-in

#### Sign In
- Navigate to http://localhost:5000/signin
- Enter email and password
- Check "Remember me" for persistent login
- Submit → Redirects to dashboard

#### Security Features
- ✅ Passwords hashed with PBKDF2-SHA256
- ✅ 260,000+ iterations for brute-force protection
- ✅ Unique salt per user
- ✅ Session-based authentication
- ✅ Protected routes require login

### 2️⃣ Property Dashboard

**URL**: http://localhost:5000/dashboard

Features:
- **Browse Properties**: 7,738+ real properties
- **Search**: Type address for autocomplete suggestions
- **Filters**: 
  - Price range (₹10L - ₹100Cr)
  - Bedrooms (1-5+)
  - Property type (Apartment, Villa, etc.)
  - Location
- **View Details**: Click property card for modal with:
  - High-resolution images
  - Full specifications
  - Exact location
  - Price breakdown

### 3️⃣ AI Price Prediction

**URL**: http://localhost:5000/price-prediction

How to Use:
1. Select location from 84+ options
2. Enter property details:
   - Bedrooms (1-10)
   - Bathrooms (1-10)
   - Balconies (0-5)
   - Built-up area (sqft)
   - Plot area (sqft)
   - Furnishing status
   - Property type
   - Parking spaces
   - Floor number
3. Click "Predict Price"
4. Get instant prediction with:
   - Estimated price
   - Price per sqft
   - Formatted display

**Model Performance**:
- Algorithm: Random Forest
- Accuracy: 99.78% (R²)
- Error: ₹2.42 Lakhs (RMSE)

**Regional Pricing**:
- South Delhi: ₹8,000/sqft
- Central Delhi: ₹7,500/sqft
- Gurgaon: ₹7,000/sqft
- North Delhi: ₹6,000/sqft
- Noida: ₹5,800/sqft
- West Delhi: ₹5,500/sqft

### 4️⃣ EMI Calculator

**URL**: http://localhost:5000/emi-calculator

Calculate:
1. Enter loan amount (₹10L - ₹10Cr)
2. Set interest rate (1% - 20%)
3. Choose tenure (1-30 years)
4. View results:
   - Monthly EMI
   - Total payment
   - Total interest
   - Visual breakdown

Example:
- Principal: ₹50,00,000
- Rate: 8.5% p.a.
- Tenure: 20 years
- **EMI**: ₹43,390/month

### 5️⃣ Interactive Map

**URL**: http://localhost:5000/map-view

Features:
- **Heatmap**: 500+ properties visualized
- **Color Gradient**: Blue (low price) → Red (high price)
- **Search**: Type address to navigate
- **Zoom**: Scroll to zoom in/out
- **Click**: Tap property for price

---

## 🛠️ Technical Details

### Architecture

```
┌─────────────────────────────────────────┐
│         User Browser (Frontend)         │
│    HTML/CSS/JS + Jinja2 Templates      │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│         Flask Web Server (Backend)      │
│  • Authentication (Flask-Login)         │
│  • Session Management                   │
│  • API Routes                           │
└─────────────┬───────────┬───────────────┘
              │           │
              ▼           ▼
      ┌───────────┐  ┌──────────────┐
      │  SQLite   │  │  ML Model    │
      │ (users.db)│  │ (Random      │
      │           │  │  Forest)     │
      └───────────┘  └──────────────┘
```

### Database Schema

**User Table** (`users.db`):
```sql
CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash VARCHAR(200) NOT NULL,
    full_name VARCHAR(150) NOT NULL,
    role VARCHAR(20) NOT NULL,  -- 'buyer' or 'seller'
    created_at DATETIME NOT NULL
);
```

### API Endpoints

| Endpoint | Method | Auth Required | Description |
|----------|--------|---------------|-------------|
| `/signup` | GET, POST | No | User registration |
| `/signin` | GET, POST | No | User login |
| `/logout` | GET | Yes | User logout |
| `/dashboard` | GET | No | Browse properties |
| `/price-prediction` | GET | Yes | Prediction form |
| `/api/predict` | POST | Yes | Get price prediction |
| `/emi-calculator` | GET | Yes | EMI calculator |
| `/api/calculate-emi` | POST | Yes | Calculate EMI |
| `/map-view` | GET | Yes | Interactive map |
| `/api/heatmap-data` | GET | Yes | Get map data |
| `/api/search-addresses` | GET | Yes | Search autocomplete |
| `/api/filter-properties` | GET | Yes | Filter properties |

### File Structure

```
d:\Sach_me_mini_project\
│
├── 📁 Authentication Files (NEW)
│   ├── database.py                 # User model
│   ├── users.db                    # SQLite database
│   ├── templates/signup.html       # Registration page
│   └── templates/signin.html       # Login page
│
├── 📁 Machine Learning
│   ├── data_preprocessing.py       # Data cleaning
│   ├── model_training.py           # Train models
│   ├── predict.py                  # Prediction logic
│   ├── house_price_model.pkl       # Trained model
│   └── Delhi_v2.csv               # Dataset (7,738 rows)
│
├── 📁 Web Application
│   ├── app.py                      # Flask backend
│   ├── templates/                  # HTML pages
│   │   ├── dashboard.html
│   │   ├── price_prediction.html
│   │   ├── emi_calculator.html
│   │   └── map_view.html
│   └── static/
│       └── css/style.css           # Styles (1,400+ lines)
│
├── 📁 Documentation
│   ├── README.md                   # Project overview
│   ├── SETUP_GUIDE.md             # This file
│   └── AUTHENTICATION_SETUP.md     # Auth docs
│
└── 📁 Configuration
    └── requirements.txt            # Python packages
```

---

## 🔐 Security Best Practices

### Current Implementation
✅ Password hashing (not stored as plain text)  
✅ SQL injection protection (SQLAlchemy)  
✅ CSRF protection (Flask built-in)  
✅ Session management (Flask-Login)  
✅ Secure cookies (Lax SameSite)  

### For Production
⚠️ **Before deploying to production**:

1. **Change Secret Key**:
   ```python
   # In app.py, replace:
   app.secret_key = os.environ.get('SECRET_KEY')
   ```

2. **Enable HTTPS Cookies**:
   ```python
   app.config['SESSION_COOKIE_SECURE'] = True
   ```

3. **Use Production Database**:
   - Replace SQLite with PostgreSQL/MySQL
   - Update connection string

4. **Add Rate Limiting**:
   ```bash
   pip install flask-limiter
   ```

5. **Enable Logging**:
   ```python
   import logging
   logging.basicConfig(level=logging.INFO)
   ```

---

## 🧪 Testing Guide

### Manual Testing Workflow

**Test 1: Sign Up**
1. Go to http://localhost:5000/signup
2. Enter:
   - Email: test@example.com
   - Password: Test123
   - Confirm: Test123
   - Name: Test User
   - Role: Buyer
3. Submit
4. ✅ Should redirect to sign-in

**Test 2: Sign In**
1. Go to http://localhost:5000/signin
2. Enter demo credentials
3. Submit
4. ✅ Should see dashboard

**Test 3: Price Prediction**
1. Click "Price Prediction" in navbar
2. Select "Dwarka, Delhi"
3. Enter: 3 BHK, 2 bath, 1200 sqft
4. Click "Predict"
5. ✅ Should see price estimate

**Test 4: Logout**
1. Click logout icon in navbar
2. ✅ Should redirect to sign-in

### API Testing

**Test Prediction API**:
```bash
# Using curl (Windows PowerShell)
$headers = @{"Content-Type"="application/json"}
$body = '{"bedrooms":3,"bathrooms":2,"area":1200}'
Invoke-RestMethod -Uri "http://localhost:5000/api/predict" -Method POST -Headers $headers -Body $body
```

**Expected Response**:
```json
{
  "success": true,
  "predicted_price": 7542000.50,
  "formatted_price": "₹75.42 Lac"
}
```

---

## 🐛 Troubleshooting

### Issue 1: "Module not found" Error

**Symptom**: `ModuleNotFoundError: No module named 'flask'`

**Solution**:
```bash
pip install -r requirements.txt
```

### Issue 2: Database Error

**Symptom**: `OperationalError: no such table: user`

**Solution**:
```bash
# Delete database
del users.db

# Restart app (will recreate)
python app.py
```

### Issue 3: Port Already in Use

**Symptom**: `OSError: [Errno 48] Address already in use`

**Solution**:
```python
# In app.py, change port:
app.run(debug=True, port=5001)
```

### Issue 4: Login Not Working

**Checklist**:
- [ ] Cookies enabled in browser?
- [ ] `app.secret_key` set in app.py?
- [ ] Flask-Login installed?
- [ ] Database has users table?

**Debug**:
```python
# Check database
python -c "from app import app, db; from database import User; app.app_context().push(); print(User.query.all())"
```

### Issue 5: Password Not Matching

**Solution**: Passwords are case-sensitive. Demo password is `demo123` (lowercase).

---

## 📈 Next Steps

### Immediate Actions
1. ✅ Sign up for a new account
2. ✅ Browse properties on dashboard
3. ✅ Try price prediction
4. ✅ Calculate EMI for your budget
5. ✅ Explore heatmap

### Future Features (Roadmap)
- [ ] Email verification on signup
- [ ] Forgot password functionality
- [ ] User profile page
- [ ] Save favorite properties
- [ ] Property comparison tool
- [ ] Price trend charts
- [ ] Neighborhood analytics
- [ ] Mobile app version

---

## 💡 Tips & Tricks

### Tip 1: Accurate Predictions
For best price predictions:
- Select exact location from dropdown
- Enter realistic property details
- Check similar properties on dashboard

### Tip 2: EMI Planning
Use EMI calculator to:
- Compare different loan tenures
- See impact of down payment
- Plan monthly budget

### Tip 3: Property Search
On dashboard:
- Use filters to narrow results
- Search by address for specific areas
- Click property cards for full details

### Tip 4: Map Exploration
On map view:
- Red areas = expensive properties
- Blue areas = affordable properties
- Search box to jump to locations

---

## 📚 Additional Resources

### Documentation
- **Authentication**: See `AUTHENTICATION_SETUP.md`
- **ML Model**: See main `README.md`
- **Flask Docs**: https://flask.palletsprojects.com/
- **scikit-learn**: https://scikit-learn.org/

### Support
- Check troubleshooting section above
- Review error messages carefully
- Ensure all dependencies installed

---

## 🎓 Learning Resources

### Want to Understand the Code?

**Flask Basics**:
- Routes: How URLs map to functions
- Templates: Jinja2 syntax
- Forms: POST request handling

**Authentication**:
- Flask-Login: User session management
- Werkzeug: Password hashing
- SQLAlchemy: Database operations

**Machine Learning**:
- Random Forest: Ensemble learning
- Feature Engineering: Data preparation
- Model Evaluation: R², RMSE metrics

**Frontend**:
- Leaflet.js: Interactive maps
- Fetch API: AJAX requests
- Modal dialogs: UI patterns

---

## 📞 Contact & Credits

**Developer**: Sach  
**Project**: Delhi House Finder  
**Version**: 2.0 (With Authentication)  
**Last Updated**: January 2025  

**Tech Stack**:
- Backend: Flask 3.1.2
- Database: SQLite + SQLAlchemy
- ML: scikit-learn 1.7.2
- Frontend: Jinja2 + Vanilla JS

---

## ✅ Completion Checklist

Mark off as you complete each step:

- [ ] Installed dependencies
- [ ] Started application
- [ ] Signed up for account
- [ ] Signed in successfully
- [ ] Browsed properties
- [ ] Tried price prediction
- [ ] Calculated EMI
- [ ] Explored map view
- [ ] Logged out and back in
- [ ] Read authentication docs

**Congratulations! You're now ready to use Delhi House Finder! 🎉**

---

*For detailed authentication documentation, see `AUTHENTICATION_SETUP.md`*  
*For ML pipeline details, see main `README.md`*
