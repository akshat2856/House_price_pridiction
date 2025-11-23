"""
Quick Start Guide - House Price Prediction Pipeline
====================================================

This script demonstrates how to use each module of the pipeline.
"""

print("="*80)
print("  HOUSE PRICE PREDICTION - QUICK START GUIDE")
print("="*80)

# ============================================================================
# OPTION 1: Run the Complete Pipeline (Train + Predict)
# ============================================================================
print("\n1. COMPLETE PIPELINE (Recommended for first run)")
print("-" * 80)
print("Command: python main.py")
print("\nThis will:")
print("  • Load and preprocess data")
print("  • Train all models")
print("  • Save the best model")
print("  • Make example predictions")

# ============================================================================
# OPTION 2: Only Train Models
# ============================================================================
print("\n2. TRAIN MODELS ONLY")
print("-" * 80)
print("Python code:")
print("""
from model_training import train_models

# Train and save best model
best_model, best_model_name, all_models, results = train_models(
    data_path='Delhi_v2.csv',
    test_size=0.2,
    random_state=42,
    save_path='house_price_model.pkl'
)

print(f"Best model: {best_model_name}")
""")

# ============================================================================
# OPTION 3: Only Make Predictions (Model must exist)
# ============================================================================
print("\n3. MAKE PREDICTIONS (Model must be trained first)")
print("-" * 80)
print("Command: python predict.py")
print("\nOr use in your code:")
print("""
from predict import HousePricePredictor

# Load the model
predictor = HousePricePredictor('house_price_model.pkl')

# Make a prediction
price = predictor.predict_single(
    area=1200,
    latitude=28.60,
    longitude=77.46,
    bedrooms=3,
    bathrooms=2,
    balcony=1,
    status='Ready to Move',
    neworold='New Property',
    parking=1,
    type_of_building='Flat'
)

print(f"Predicted Price: ₹{price:,.2f}")
""")

# ============================================================================
# OPTION 4: Only Preprocess Data
# ============================================================================
print("\n4. PREPROCESS DATA ONLY")
print("-" * 80)
print("""
from data_preprocessing import preprocess_data

# Get preprocessed data
X_train, X_test, y_train, y_test, preprocessor, features = preprocess_data(
    data_path='Delhi_v2.csv',
    test_size=0.2,
    random_state=42
)

print(f"Training samples: {len(X_train)}")
print(f"Features: {len(features)}")
""")

# ============================================================================
# OPTION 5: Batch Predictions from CSV
# ============================================================================
print("\n5. BATCH PREDICTIONS FROM CSV FILE")
print("-" * 80)
print("""
from predict import HousePricePredictor

predictor = HousePricePredictor('house_price_model.pkl')

# Make predictions on multiple houses
results = predictor.predict_batch(
    input_file='new_houses.csv',
    output_file='predictions.csv'
)
""")

# ============================================================================
# OPTION 6: Custom Feature Engineering
# ============================================================================
print("\n6. CUSTOM FEATURE ENGINEERING")
print("-" * 80)
print("""
from data_preprocessing import HousePricePreprocessor

# Create preprocessor with custom settings
preprocessor = HousePricePreprocessor(
    data_path='Delhi_v2.csv',
    target_column='price',
    random_state=42
)

# Run individual steps
preprocessor.load_data()
preprocessor.clean_data()
preprocessor.engineer_features()

# Add your custom features here
preprocessor.df['custom_feature'] = preprocessor.df['area'] / preprocessor.df['Bedrooms']

# Continue with the pipeline
X_train, X_test, y_train, y_test = preprocessor.prepare_data()
""")

# ============================================================================
# MODEL PERFORMANCE SUMMARY
# ============================================================================
print("\n" + "="*80)
print("  MODEL PERFORMANCE SUMMARY (from last run)")
print("="*80)
print("""
Model              | Test R²  | Test RMSE        | Training Time
-------------------|----------|------------------|---------------
Random Forest      | 0.9978   | ₹2,42,368        | ~15-30 sec
XGBoost            | 0.9952   | ₹3,56,330        | ~5-15 sec
Linear Regression  | 0.9532   | ₹11,16,933       | <1 sec

Best Model: Random Forest
""")

# ============================================================================
# FILE STRUCTURE
# ============================================================================
print("\n" + "="*80)
print("  PROJECT FILES")
print("="*80)
print("""
Core Modules:
  • data_preprocessing.py    - Data cleaning & feature engineering
  • model_training.py        - Model training & evaluation
  • predict.py               - Making predictions
  • utils.py                 - Helper functions
  • main.py                  - Complete pipeline runner

Data & Model:
  • Delhi_v2.csv             - Original dataset
  • house_price_model.pkl    - Trained model (generated)

Visualizations:
  • random_forest_feature_importance.png
  • xgboost_feature_importance.png
  • random_forest_predictions.png

Documentation:
  • README.md                - Full documentation
  • requirements.txt         - Python packages
  • quick_start.py           - This guide
""")

# ============================================================================
# DEPLOYMENT EXAMPLE
# ============================================================================
print("\n" + "="*80)
print("  DEPLOYMENT EXAMPLE (Flask API)")
print("="*80)
print("""
# app.py
from flask import Flask, request, jsonify
from predict import HousePricePredictor

app = Flask(__name__)
predictor = HousePricePredictor('house_price_model.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    price = predictor.predict_single(**data)
    return jsonify({
        'predicted_price': float(price),
        'formatted_price': f'₹{price:,.2f}'
    })

if __name__ == '__main__':
    app.run(debug=True)

# Usage:
# curl -X POST http://localhost:5000/predict \\
#      -H "Content-Type: application/json" \\
#      -d '{"area": 1200, "latitude": 28.6, "longitude": 77.4, 
#           "bedrooms": 3, "bathrooms": 2}'
""")

# ============================================================================
# TIPS & BEST PRACTICES
# ============================================================================
print("\n" + "="*80)
print("  TIPS & BEST PRACTICES")
print("="*80)
print("""
1. Always use the same random_state for reproducibility
2. Don't modify the preprocessor after training
3. All input features must match training data format
4. Check for outliers in your input data
5. Model works best for Delhi NCR region properties
6. Retrain periodically with new data for better accuracy
7. Use cross-validation for more robust evaluation
8. Monitor prediction confidence/variance
""")

print("\n" + "="*80)
print("  Ready to get started? Run: python main.py")
print("="*80 + "\n")
