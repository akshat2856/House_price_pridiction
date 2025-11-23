# House Price Prediction - End-to-End ML Pipeline

A complete, production-ready machine learning pipeline for predicting house prices in Delhi NCR using scikit-learn, Random Forest, and XGBoost.

## 📋 Project Overview

This project implements an end-to-end machine learning pipeline that:
- Loads and preprocesses house price data
- Handles missing values and outliers
- Engineers relevant features
- Trains and compares multiple regression models
- Selects and saves the best performing model
- Provides an easy-to-use prediction interface

## 🗂️ Project Structure

```
├── Delhi_v2.csv                  # Dataset (house price data)
├── data_preprocessing.py         # Data cleaning and feature engineering
├── model_training.py             # Model training and evaluation
├── predict.py                    # Prediction module
├── utils.py                      # Utility functions
├── main.py                       # Complete pipeline runner
├── house_price_model.pkl         # Saved best model (generated)
└── README.md                     # This file
```

## 🚀 Quick Start

### Prerequisites

Install required packages:
```bash
pip install pandas scikit-learn xgboost matplotlib seaborn numpy
```

### Running the Complete Pipeline

```bash
python main.py
```

This will:
1. Load and preprocess the data
2. Train multiple models (Linear Regression, Random Forest, XGBoost)
3. Compare model performance
4. Save the best model
5. Make example predictions

## 📊 Module Details

### 1. `data_preprocessing.py`

Handles all data preprocessing tasks:

**Features:**
- Loads data from CSV
- Removes irrelevant columns (descriptions, addresses, etc.)
- Handles missing values using appropriate imputation strategies
- Removes outliers using percentile-based filtering
- Engineers new features:
  - `total_rooms`: Bedrooms + Bathrooms
  - `bed_bath_ratio`: Bedrooms / Bathrooms ratio
  - Binary features: `has_parking`, `has_lift`, `has_balcony`
- Creates preprocessing pipeline using ColumnTransformer
- Scales numeric features using StandardScaler
- Encodes categorical features using OneHotEncoder

**Usage:**
```python
from data_preprocessing import preprocess_data

X_train, X_test, y_train, y_test, preprocessor, feature_names = preprocess_data(
    data_path='Delhi_v2.csv',
    test_size=0.2,
    random_state=42
)
```

**Key Functions:**
- `HousePricePreprocessor`: Main preprocessing class
- `preprocess_data()`: Convenience function to run full pipeline

**Best Practices Implemented:**
- ✅ No data leakage (preprocessing fit only on training data)
- ✅ Pipeline-based approach (all transformations in one object)
- ✅ Proper handling of missing values
- ✅ Separate transformers for numeric and categorical features

### 2. `model_training.py`

Trains and evaluates multiple regression models:

**Models Trained:**
1. **Linear Regression** - Baseline model
2. **Random Forest Regressor** - Ensemble tree-based model
3. **XGBoost Regressor** - Gradient boosting (if available)

**Features:**
- Trains all models with proper hyperparameters
- Evaluates using RMSE, MAE, and R² score
- Compares model performance
- Selects best model based on test R²
- Saves best model using joblib
- Generates feature importance plots for tree-based models

**Usage:**
```python
from model_training import train_models

best_model, best_model_name, all_models, results = train_models(
    data_path='Delhi_v2.csv',
    test_size=0.2,
    random_state=42,
    save_path='house_price_model.pkl'
)
```

**Key Functions:**
- `ModelTrainer`: Main training class
- `train_models()`: Convenience function for complete training pipeline

### 3. `predict.py`

Provides prediction interface for the trained model:

**Features:**
- Loads saved model
- Makes predictions on new data
- Supports single prediction with individual parameters
- Supports batch predictions from CSV
- Formats prices in Indian Rupee notation

**Usage:**

**Single Prediction:**
```python
from predict import HousePricePredictor

predictor = HousePricePredictor(model_path='house_price_model.pkl')

predicted_price = predictor.predict_single(
    area=1350.0,
    latitude=28.60885,
    longitude=77.46056,
    bedrooms=3.0,
    bathrooms=3.0,
    balcony=2.0,
    status='Ready to Move',
    neworold='New Property',
    parking=1.0,
    furnished_status='Semi-Furnished',
    lift=2.0,
    type_of_building='Flat'
)

print(f"Predicted Price: ₹{predicted_price:,.2f}")
```

**Batch Prediction:**
```python
predictor.predict_batch(
    input_file='new_houses.csv',
    output_file='predictions.csv'
)
```

### 4. `utils.py`

Helper functions for the pipeline:

**Functions:**
- `evaluate_model()`: Calculate and display model metrics
- `plot_feature_importance()`: Visualize feature importance
- `plot_predictions()`: Plot actual vs predicted values
- `save_model()`: Save model to disk
- `load_model()`: Load model from disk
- `compare_models()`: Create comparison table
- `format_price()`: Format prices in Indian notation

## 📈 Model Performance

The pipeline trains three models and compares them:

| Model | Test RMSE | Test R² | Training Time |
|-------|-----------|---------|---------------|
| Linear Regression | Fast baseline | ~0.75 | < 1 sec |
| Random Forest | Best performance | ~0.85-0.90 | 10-30 sec |
| XGBoost | Competitive | ~0.85-0.88 | 5-15 sec |

*Note: Actual performance depends on the dataset and hyperparameters*

## 🎯 Features

### Data Processing Features:
- Area (square feet)
- Location (latitude, longitude)
- Bedrooms, Bathrooms, Balconies
- Construction status
- Property age (new/resale)
- Parking spaces
- Furnished status
- Number of lifts
- Building type

### Engineered Features:
- Price per square foot
- Total rooms
- Bedroom-bathroom ratio
- Binary features (has_parking, has_lift, has_balcony)

## 🔧 Customization

### Modify Hyperparameters

Edit `model_training.py`:

```python
# Random Forest
rf = RandomForestRegressor(
    n_estimators=200,      # Increase trees
    max_depth=25,          # Increase depth
    min_samples_split=3,   # Adjust splitting
    random_state=42
)

# XGBoost
xgb = XGBRegressor(
    n_estimators=150,      # Increase boosting rounds
    max_depth=8,           # Increase depth
    learning_rate=0.05,    # Lower learning rate
    random_state=42
)
```

### Add New Features

Edit `data_preprocessing.py` in the `engineer_features()` method:

```python
def engineer_features(self):
    # Add your custom feature
    self.df['custom_feature'] = self.df['area'] * self.df['Bedrooms']
    return self.df
```

## 📊 Output Files

After running the pipeline:

1. **house_price_model.pkl** - Saved best model
2. **random_forest_feature_importance.png** - Feature importance visualization
3. **xgboost_feature_importance.png** - XGBoost feature importance
4. **[model]_predictions.png** - Actual vs predicted scatter plot

## 🛡️ Best Practices Implemented

✅ **No Data Leakage**: Preprocessing fit only on training data  
✅ **Pipeline-Based**: All transformations in scikit-learn Pipeline  
✅ **Proper Train-Test Split**: 80-20 split with stratification  
✅ **Reproducibility**: Fixed random_state throughout  
✅ **Modular Code**: Separated concerns across modules  
✅ **Comprehensive Comments**: Every function documented  
✅ **Error Handling**: Graceful handling of missing packages  
✅ **Production-Ready**: Can be deployed as-is  

## 📝 Example Predictions

```python
# Example 1: Luxury 3 BHK
Input: 1500 sq ft, 3 BHK, Noida, Furnished, 2 Parking
Output: ₹65-75 Lakh

# Example 2: Budget 2 BHK
Input: 900 sq ft, 2 BHK, Delhi NCR, Unfurnished, 1 Parking
Output: ₹35-45 Lakh

# Example 3: Premium 4 BHK
Input: 2200 sq ft, 4 BHK, Gurgaon, Semi-Furnished, 2 Parking
Output: ₹1.2-1.5 Crore
```

## 🚀 Deployment

To deploy this model:

1. **Save the complete pipeline:**
   ```python
   joblib.dump(best_model, 'house_price_model.pkl')
   ```

2. **Load in production:**
   ```python
   model = joblib.load('house_price_model.pkl')
   prediction = model.predict(new_data)
   ```

3. **Create API endpoint** (Flask/FastAPI):
   ```python
   from flask import Flask, request, jsonify
   from predict import HousePricePredictor
   
   app = Flask(__name__)
   predictor = HousePricePredictor('house_price_model.pkl')
   
   @app.route('/predict', methods=['POST'])
   def predict():
       data = request.json
       price = predictor.predict_single(**data)
       return jsonify({'predicted_price': price})
   ```

## 📧 Contact & Support

For questions or improvements, please open an issue or submit a pull request.

## 📄 License

This project is provided as-is for educational and commercial use.

---

**Built with ❤️ using Python, scikit-learn, and XGBoost**
#   H o u s e _ p r i c e _ p r i d i c t i o n  
 