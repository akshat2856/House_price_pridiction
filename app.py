"""
Flask Web Application for House Price Prediction
Integrates the trained ML model with a beautiful web interface
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from functools import wraps
import pandas as pd
import numpy as np
from predict import HousePricePredictor, format_price
from database import db, User
import json
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production-2024'  # Change this in production
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'signin'
login_manager.login_message = 'Please sign in to access this page.'
login_manager.login_message_category = 'info'

# Initialize the predictor
predictor = HousePricePredictor('house_price_model.pkl')

# Load dataset for location data
df = pd.read_csv('Delhi_v2.csv')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    """Landing page - redirect to dashboard or signin"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('dashboard'))  # Allow viewing dashboard without login


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Sign up page"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        full_name = request.form.get('full_name')
        role = request.form.get('role', 'buyer')
        
        # Validation
        if not email or not password or not full_name:
            flash('All fields are required', 'danger')
            return render_template('signup.html')
        
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return render_template('signup.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long', 'danger')
            return render_template('signup.html')
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered. Please sign in.', 'warning')
            return redirect(url_for('signin'))
        
        # Create new user
        new_user = User(email=email, full_name=full_name, role=role)
        new_user.set_password(password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully! Please sign in.', 'success')
            return redirect(url_for('signin'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred. Please try again.', 'danger')
            print(f"Error creating user: {e}")
            return render_template('signup.html')
    
    return render_template('signup.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    """Sign in page"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember_me')
        
        if not email or not password:
            flash('Email and password are required', 'danger')
            return render_template('signin.html')
        
        # Find user in database
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user, remember=bool(remember))
            flash(f'Welcome back, {user.full_name}!', 'success')
            
            # Redirect to next page or dashboard
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'danger')
            return render_template('signin.html')
    
    return render_template('signin.html')


@app.route('/logout')
@login_required
def logout():
    """Logout user"""
    logout_user()
    flash('You have been logged out successfully', 'success')
    return redirect(url_for('signin'))


@app.route('/dashboard')
def dashboard():
    """Main dashboard page - accessible to all, but shows different content for authenticated users"""
    return render_template('dashboard.html', user=current_user)


@app.route('/price-prediction')
@login_required
def price_prediction():
    """Price prediction page - requires authentication"""
    # Get unique locations from dataset
    locations = df.groupby(['latitude', 'longitude']).first().reset_index()[['latitude', 'longitude']].head(50).to_dict('records')
    return render_template('price_prediction.html', locations=locations, user=current_user)


@app.route('/api/predict', methods=['POST'])
@login_required
def api_predict():
    """API endpoint for price prediction"""
    try:
        data = request.json
        
        # Extract features from request
        area = float(data.get('area', 1000))
        latitude = float(data.get('latitude', 28.6))
        longitude = float(data.get('longitude', 77.4))
        bedrooms = float(data.get('bedrooms', 2))
        bathrooms = float(data.get('bathrooms', 2))
        balcony = float(data.get('balcony', 1)) if data.get('balcony') else None
        status = data.get('status')
        neworold = data.get('neworold')
        parking = float(data.get('parking', 0)) if data.get('parking') else None
        furnished_status = data.get('furnished_status')
        lift = float(data.get('lift', 0)) if data.get('lift') else None
        type_of_building = data.get('type_of_building', 'Flat')
        
        # Make prediction
        predicted_price = predictor.predict_single(
            area=area,
            latitude=latitude,
            longitude=longitude,
            bedrooms=bedrooms,
            bathrooms=bathrooms,
            balcony=balcony,
            status=status,
            neworold=neworold,
            parking=parking,
            furnished_status=furnished_status,
            lift=lift,
            type_of_building=type_of_building
        )
        
        return jsonify({
            'success': True,
            'predicted_price': float(predicted_price),
            'formatted_price': format_price(predicted_price)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/locations')
@login_required
def api_locations():
    """Get available locations for dropdown"""
    # Get unique locations with addresses
    locations_df = df[['latitude', 'longitude', 'Address']].drop_duplicates().head(100)
    locations = locations_df.to_dict('records')
    return jsonify(locations)


@app.route('/api/heatmap-data')
@login_required
def api_heatmap_data():
    """Get data for heatmap visualization"""
    # Sample data points for heatmap (latitude, longitude, price)
    heatmap_data = df[['latitude', 'longitude', 'price']].dropna().head(500)
    
    # Normalize prices for intensity
    max_price = heatmap_data['price'].max()
    heatmap_data['intensity'] = heatmap_data['price'] / max_price
    
    data = heatmap_data.to_dict('records')
    return jsonify(data)


@app.route('/api/search-addresses')
@login_required
def api_search_addresses():
    """Search addresses based on query"""
    query = request.args.get('q', '').lower()
    
    if not query or len(query) < 2:
        return jsonify([])
    
    # Get unique addresses from dataset
    addresses = df[['Address', 'latitude', 'longitude']].drop_duplicates()
    
    # Filter addresses that contain the query
    filtered = addresses[addresses['Address'].str.lower().str.contains(query, na=False)]
    
    # Limit to 10 results
    results = filtered.head(10).to_dict('records')
    
    return jsonify(results)


@app.route('/api/property/<int:property_id>')
@login_required
def api_property_details(property_id):
    """Get detailed property information"""
    if property_id >= len(df):
        return jsonify({'success': False, 'error': 'Property not found'}), 404
    
    property_data = df.iloc[property_id].to_dict()
    
    # Convert NaN to None for JSON serialization
    property_data = {k: (None if pd.isna(v) else v) for k, v in property_data.items()}
    
    return jsonify({
        'success': True,
        'property': property_data
    })


@app.route('/api/filter-properties')
def api_filter_properties():
    """Filter properties based on criteria - accessible to all users"""
    # Get filter parameters
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    bedrooms = request.args.get('bedrooms', type=int)
    property_type = request.args.get('property_type', '')
    location = request.args.get('location', '')
    
    # Start with full dataset
    filtered_df = df.copy()
    
    # Apply filters
    if min_price:
        filtered_df = filtered_df[filtered_df['price'] >= min_price]
    if max_price:
        filtered_df = filtered_df[filtered_df['price'] <= max_price]
    if bedrooms:
        filtered_df = filtered_df[filtered_df['Bedrooms'] == bedrooms]
    if property_type:
        filtered_df = filtered_df[filtered_df['type_of_building'].str.contains(property_type, case=False, na=False)]
    if location:
        filtered_df = filtered_df[filtered_df['Address'].str.contains(location, case=False, na=False)]
    
    # Get first 20 results
    results = filtered_df.head(20).to_dict('records')
    
    # Convert NaN to None
    results = [{k: (None if pd.isna(v) else v) for k, v in prop.items()} for prop in results]
    
    return jsonify({
        'success': True,
        'count': len(filtered_df),
        'properties': results
    })


@app.route('/emi-calculator')
@login_required
def emi_calculator():
    """EMI Calculator page"""
    return render_template('emi_calculator.html', user=current_user)


@app.route('/budget-calculator')
@login_required
def budget_calculator():
    """Budget Calculator page"""
    return render_template('budget_calculator.html', user=current_user)


@app.route('/loan-eligibility')
@login_required
def loan_eligibility():
    """Loan Eligibility Calculator page"""
    return render_template('loan_eligibility.html', user=current_user)


@app.route('/area-converter')
@login_required
def area_converter():
    """Area Converter page"""
    return render_template('area_converter.html', user=current_user)


@app.route('/api/calculate-emi', methods=['POST'])
@login_required
def api_calculate_emi():
    """Calculate EMI"""
    try:
        data = request.json
        principal = float(data.get('principal', 5000000))
        rate = float(data.get('rate', 8.5)) / 100 / 12  # Monthly rate
        tenure = int(data.get('tenure', 20)) * 12  # Months
        
        # EMI calculation formula
        emi = principal * rate * ((1 + rate) ** tenure) / (((1 + rate) ** tenure) - 1)
        
        total_amount = emi * tenure
        total_interest = total_amount - principal
        
        return jsonify({
            'success': True,
            'emi': round(emi, 2),
            'total_amount': round(total_amount, 2),
            'total_interest': round(total_interest, 2),
            'principal': round(principal, 2)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/map-view')
@login_required
def map_view():
    """Map view with heatmap"""
    # Get lat/lng from query params if provided
    lat = request.args.get('lat', 28.6139)
    lng = request.args.get('lng', 77.2090)
    zoom = request.args.get('zoom', 11)
    
    return render_template('map_view.html', user=current_user, lat=lat, lng=lng, zoom=zoom)


def init_database():
    """Initialize database and create tables"""
    with app.app_context():
        db.create_all()
        print("✅ Database tables created successfully!")
        
        # Check if demo users already exist
        if User.query.filter_by(email='demo@delhihouse.com').first() is None:
            # Create demo buyer account
            demo_buyer = User(
                email='demo@delhihouse.com',
                full_name='Demo Buyer',
                role='buyer'
            )
            demo_buyer.set_password('demo123')
            db.session.add(demo_buyer)
            
            # Create demo seller account
            demo_seller = User(
                email='seller@delhihouse.com',
                full_name='Demo Seller',
                role='seller'
            )
            demo_seller.set_password('seller123')
            db.session.add(demo_seller)
            
            db.session.commit()
            print("✅ Demo accounts created successfully!")
        else:
            print("ℹ️  Demo accounts already exist")


if __name__ == '__main__':
    # Create templates and static folders if they don't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('static/images', exist_ok=True)
    
    # Initialize database
    init_database()
    
    print("="*80)
    print("  HOMEAI - AI-POWERED PROPERTY PLATFORM")
    print("="*80)
    print("\n🚀 Starting Flask server...")
    print("\n📧 Demo Accounts:")
    print("   Buyer:  demo@homeai.com     | Password: demo123")
    print("   Seller: seller@homeai.com   | Password: seller123")
    print("\n🌐 Open in browser: http://localhost:5000")
    print("="*80 + "\n")
    
    # Run with Flask's built-in server
    app.run(host='127.0.0.1', port=5000, debug=True)
