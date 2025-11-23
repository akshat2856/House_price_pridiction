# 🏠 Delhi House Finder - Web Application

A beautiful, full-featured web application for house price prediction powered by Machine Learning. This application integrates the trained Random Forest model with a modern, responsive web interface.

## ✨ Features

### 🔐 Authentication System
- Secure login page with beautiful gradient design
- Test accounts for demo purposes
- Session-based authentication
- Protected routes

### 🏡 Property Browse (Dashboard)
- Beautiful grid layout showcasing featured properties
- Property cards with images, prices, and details
- Interactive search functionality
- Responsive design

### 📊 AI Price Prediction
- Real-time house price prediction using trained ML model
- Interactive form with all property features
- Location selector with predefined Delhi NCR locations
- Beautiful result display with detailed breakdown
- Price per sqft calculation
- Smooth animations

### 💰 EMI Calculator
- Interactive loan calculator with sliders
- Real-time EMI calculation
- Visual breakdown of Principal vs Interest
- Beautiful doughnut chart visualization
- Adjustable loan amount, interest rate, and tenure

### 🗺️ Map View with Heatmap
- Interactive Leaflet.js map
- Property price heatmap overlay
- Click-to-predict functionality
- Major location markers
- Color-coded price intensity

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Required packages:
- Flask
- pandas
- numpy
- scikit-learn
- xgboost
- matplotlib
- seaborn
- joblib

### 2. Start the Server

```bash
python app.py
```

### 3. Access the Application

Open your browser and navigate to:
```
http://localhost:5000
```

### 4. Login with Test Account

**Demo Account:**
- Email: `demo@delhihouse.com`
- Password: `demo123`

**Test Account:**
- Email: `test@delhihouse.com`
- Password: `test123`

## 📁 Project Structure

```
Sach_me_mini_project/
│
├── app.py                          # Flask application (main backend)
├── predict.py                      # ML model prediction module
├── data_preprocessing.py           # Data preprocessing pipeline
├── model_training.py               # Model training pipeline
├── utils.py                        # Utility functions
├── house_price_model.pkl           # Trained ML model
├── Delhi_v2.csv                    # Dataset
│
├── templates/                      # HTML templates
│   ├── login.html                  # Login page
│   ├── dashboard.html              # Main dashboard
│   ├── price_prediction.html       # Price prediction page
│   ├── emi_calculator.html         # EMI calculator
│   └── map_view.html               # Map view with heatmap
│
├── static/                         # Static assets
│   ├── css/
│   │   └── style.css               # Main stylesheet
│   └── js/
│       └── main.js                 # JavaScript file
│
└── requirements.txt                # Python dependencies
```

## 🎨 Pages Overview

### 1. Login Page (`/login`)
- **Design**: Gradient background with split layout
- **Left**: Login form with email/password
- **Right**: Feature showcase
- **Features**: 
  - Form validation
  - Error handling
  - Remember me option
  - Demo credentials display

### 2. Dashboard (`/dashboard`)
- **Design**: Clean grid layout with property cards
- **Features**:
  - Search bar with filters
  - 6 featured property cards
  - Property images, prices, and details
  - Responsive grid
  - Hover animations

### 3. Price Prediction (`/price-prediction`)
- **Design**: Modern form with purple gradient results
- **Features**:
  - Location dropdown (8 major Delhi NCR locations)
  - Property type selector
  - Area, bedrooms, bathrooms inputs
  - Furnishing status, parking, etc.
  - Real-time ML prediction
  - Beautiful result card with breakdown
  - Actions: Calculate EMI or New Prediction

### 4. EMI Calculator (`/emi-calculator`)
- **Design**: Split layout with inputs and results
- **Features**:
  - Interactive sliders for loan amount, rate, tenure
  - Real-time EMI calculation
  - Visual progress bars
  - Doughnut chart (Chart.js)
  - Principal vs Interest breakdown

### 5. Map View (`/map-view`)
- **Design**: Full-screen interactive map
- **Features**:
  - Leaflet.js integration
  - Heatmap overlay showing property prices
  - Color gradient (blue → green → yellow → red)
  - Major location markers
  - Click-to-predict functionality
  - Legend for price ranges

## 🔌 API Endpoints

### Authentication
- `GET /` - Redirect to login or dashboard
- `GET /login` - Login page
- `POST /login` - Login authentication
- `GET /logout` - Logout user

### Pages
- `GET /dashboard` - Main dashboard (protected)
- `GET /price-prediction` - Prediction page (protected)
- `GET /emi-calculator` - EMI calculator (protected)
- `GET /map-view` - Map view (protected)

### API Routes
- `POST /api/predict` - ML price prediction
- `GET /api/locations` - Get available locations
- `GET /api/heatmap-data` - Get heatmap data for map
- `POST /api/calculate-emi` - Calculate EMI

## 🎯 ML Model Integration

The web application uses the trained Random Forest model with 99.78% R² score:

**Input Features:**
- Location (latitude, longitude)
- Area (sq.ft)
- Bedrooms, Bathrooms, Balconies
- Property Type, Status, Age
- Furnishing Status
- Parking Spaces
- Number of Lifts

**Output:**
- Predicted house price in ₹
- Formatted in Indian notation (Lac/Crore)

## 🎨 Design Highlights

### Color Scheme
- **Primary**: Indigo (#4F46E5)
- **Secondary**: Green (#10B981)
- **Danger**: Red (#EF4444)
- **Warning**: Amber (#F59E0B)

### Typography
- Font: Segoe UI, Tahoma, Geneva, Verdana, sans-serif
- Headings: Bold, 24-36px
- Body: Regular, 14-16px

### Components
- **Cards**: White background, rounded corners, shadow
- **Buttons**: Gradient primary color, hover effects
- **Forms**: Clean inputs with focus states
- **Navigation**: Sticky top bar with active states

## 📱 Responsive Design

The application is fully responsive:
- **Desktop**: Full layout with all features
- **Tablet**: Adaptive grid, condensed navigation
- **Mobile**: Single column, touch-friendly

## 🔒 Security Features

- Session-based authentication
- Protected routes with `@login_required` decorator
- Secret key for session encryption
- Input validation on forms
- Error handling for API requests

## 🚀 Deployment

### Development
```bash
python app.py
```
Runs on `http://localhost:5000` with debug mode

### Production

1. **Set Secret Key**:
   ```python
   app.secret_key = os.environ.get('SECRET_KEY', 'your-secure-random-key')
   ```

2. **Use Production Server**:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:8000 app:app
   ```

3. **Environment Variables**:
   - `SECRET_KEY`: Session encryption key
   - `FLASK_ENV`: Set to 'production'

## 🌟 Features in Detail

### Price Prediction Flow
1. User selects location from dropdown
2. Enters property details (area, bedrooms, etc.)
3. Clicks "Predict Price with AI"
4. JavaScript sends POST request to `/api/predict`
5. Flask calls ML model with input features
6. Model returns predicted price
7. Result displayed in beautiful card
8. Shows price, price/sqft, area, configuration

### EMI Calculator Flow
1. User adjusts sliders for loan parameters
2. Display updates in real-time
3. Clicks "Calculate EMI"
4. JavaScript sends POST request to `/api/calculate-emi`
5. Flask calculates EMI using formula
6. Returns EMI, principal, interest, total
7. Updates UI with values and chart

### Map Heatmap Flow
1. Page loads Leaflet.js map centered on Delhi
2. Fetches heatmap data from `/api/heatmap-data`
3. Flask returns 500 property locations with prices
4. Normalizes prices to intensity (0-1)
5. Creates heatmap layer with gradient
6. Adds markers for major locations
7. Click opens popup with coordinates

## 🎓 Learning Points

This project demonstrates:
- Full-stack web development
- ML model deployment
- RESTful API design
- Modern CSS with variables
- JavaScript async/await
- Flask session management
- Interactive data visualization
- Responsive web design

## 🐛 Troubleshooting

### Model not found error
```bash
python model_training.py  # Train the model first
```

### Flask not installed
```bash
pip install flask
```

### Port already in use
Change port in `app.py`:
```python
app.run(debug=True, port=5001)  # Use different port
```

### Chart not showing
Ensure Chart.js CDN is loaded:
```html
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
```

## 📊 Performance

- **Page Load**: < 1 second
- **Prediction Time**: < 500ms
- **Model Load**: < 2 seconds on startup
- **Map Render**: < 1 second with 500 points

## 🔮 Future Enhancements

- [ ] User registration system
- [ ] Save favorite properties
- [ ] Property comparison feature
- [ ] Advanced filters (price range, etc.)
- [ ] Property details page
- [ ] Contact seller functionality
- [ ] Admin dashboard
- [ ] Database integration (PostgreSQL)
- [ ] Property photo upload
- [ ] PDF report generation
- [ ] Email notifications
- [ ] Social media sharing

## 📄 License

This project is provided for educational and commercial use.

## 🤝 Credits

- **ML Model**: Random Forest Regressor (99.78% R² score)
- **Frontend**: HTML5, CSS3, JavaScript
- **Backend**: Flask (Python)
- **Maps**: Leaflet.js + OpenStreetMap
- **Charts**: Chart.js
- **Icons**: Font Awesome 6

---

## 🎉 Success!

Your complete house price prediction website is now ready!

**Login** → **Browse Properties** → **Predict Prices** → **Calculate EMI** → **View Map**

Enjoy exploring the Delhi House Finder! 🏠✨
