"""
Prediction module for house price prediction.
Loads trained model and makes predictions on new data.
"""

import pandas as pd
import numpy as np
from utils import load_model
import warnings
warnings.filterwarnings('ignore')


class HousePricePredictor:
    """
    Handles loading the trained model and making predictions.
    """
    
    def __init__(self, model_path='house_price_model.pkl'):
        """
        Initialize the predictor by loading the trained model.
        
        Parameters:
        -----------
        model_path : str
            Path to the saved model file
        """
        self.model_path = model_path
        self.model = None
        self.load_trained_model()
    
    def load_trained_model(self):
        """
        Load the trained model from disk.
        """
        print(f"Loading model from: {self.model_path}")
        self.model = load_model(self.model_path)
        print("Model loaded and ready for predictions!")
    
    def predict(self, input_data):
        """
        Make predictions on new data.
        
        Parameters:
        -----------
        input_data : pd.DataFrame or dict
            Input features for prediction
            If dict, will be converted to DataFrame
            
        Returns:
        --------
        np.ndarray : Predicted prices
        """
        if self.model is None:
            raise ValueError("Model not loaded. Please check the model path.")
        
        # Convert dict to DataFrame if necessary
        if isinstance(input_data, dict):
            input_data = pd.DataFrame([input_data])
        
        # Make prediction
        predictions = self.model.predict(input_data)
        
        return predictions
    
    def predict_single(self, area, latitude, longitude, bedrooms, bathrooms,
                       balcony=None, status=None, neworold=None, parking=None,
                       furnished_status=None, lift=None, type_of_building=None,
                       price_sqft=None):
        """
        Make a prediction for a single house with individual parameters.
        
        Parameters:
        -----------
        area : float
            Area of the property in square feet
        latitude : float
            Latitude coordinate
        longitude : float
            Longitude coordinate
        bedrooms : float
            Number of bedrooms
        bathrooms : float
            Number of bathrooms
        balcony : float, optional
            Number of balconies
        status : str, optional
            Construction status (e.g., 'Ready to Move', 'Under Construction')
        neworold : str, optional
            Property age status (e.g., 'New Property', 'Resale')
        parking : float, optional
            Number of parking spaces
        furnished_status : str, optional
            Furnishing status (e.g., 'Furnished', 'Semi-Furnished', 'Unfurnished')
        lift : float, optional
            Number of lifts
        type_of_building : str, optional
            Type of building (e.g., 'Flat', 'Villa')
        price_sqft : float, optional
            Price per square foot
            
        Returns:
        --------
        float : Predicted price
        """
        # Set defaults for optional parameters
        if balcony is None:
            balcony = 0.0
        if parking is None:
            parking = 0.0
        if lift is None:
            lift = 0.0
        if status is None:
            status = 'Unknown'
        if neworold is None:
            neworold = 'Unknown'
        if furnished_status is None:
            furnished_status = 'Unknown'
        if type_of_building is None:
            type_of_building = 'Flat'
        
        # Calculate price_sqft if not provided - estimate based on location and features
        if price_sqft is None:
            # Base price per sqft based on premium location (latitude/longitude)
            base_price = 0.0
            
            # PREMIUM LOCATIONS - Higher base pricing (adjusted for 2025 market rates)
            # South Delhi (Vasant Kunj, GK, Hauz Khas, Saket, Defence Colony)
            if 28.50 <= latitude <= 28.60 and 77.15 <= longitude <= 77.30:
                base_price = 16800.0  # Premium South Delhi (₹12,000 * 1.4)
            # Central Delhi (Connaught Place, Chanakyapuri, Lutyens)
            elif 28.60 <= latitude <= 28.68 and 77.18 <= longitude <= 77.25:
                base_price = 21000.0  # Ultra Premium Central Delhi (₹15,000 * 1.4)
            # Gurgaon Golf Course Road, DLF Phase 1-5
            elif 28.40 <= latitude <= 28.50 and 77.05 <= longitude <= 77.15:
                base_price = 15400.0  # Premium Gurgaon (₹11,000 * 1.4)
            # Gurgaon Cyber City, MG Road
            elif 28.35 <= latitude <= 28.45 and 76.95 <= longitude <= 77.10:
                base_price = 13300.0  # Gurgaon Business District (₹9,500 * 1.4)
            
            # MID-PREMIUM LOCATIONS
            # West Delhi (Dwarka, Janakpuri, Punjabi Bagh)
            elif 28.55 <= latitude <= 28.65 and 77.00 <= longitude <= 77.15:
                base_price = 10500.0  # West Delhi (₹7,500 * 1.4)
            # North Delhi (Rohini, Pitampura, Model Town)
            elif 28.65 <= latitude <= 28.72 and 77.10 <= longitude <= 77.25:
                base_price = 11200.0  # North Delhi (₹8,000 * 1.4)
            # Noida Sectors (62-78, Expressway)
            elif 28.55 <= latitude <= 28.62 and 77.35 <= longitude <= 77.40:
                base_price = 11900.0  # Premium Noida (₹8,500 * 1.4)
            # Noida General Sectors
            elif 28.50 <= latitude <= 28.62 and 77.30 <= longitude <= 77.40:
                base_price = 9100.0  # Noida (₹6,500 * 1.4)
            
            # STANDARD LOCATIONS
            # Greater Noida West (Noida Extension)
            elif 28.45 <= latitude <= 28.55 and 77.40 <= longitude <= 77.50:
                base_price = 6300.0  # Greater Noida West (₹4,500 * 1.4)
            # Greater Noida (Alpha, Beta, Gamma)
            elif 28.45 <= latitude <= 28.62 and 77.45 <= longitude <= 77.55:
                base_price = 7700.0  # Greater Noida (₹5,500 * 1.4)
            # Ghaziabad (Vaishali, Indirapuram, Vasundhara)
            elif 28.62 <= latitude <= 28.70 and 77.35 <= longitude <= 77.45:
                base_price = 8400.0  # Ghaziabad (₹6,000 * 1.4)
            # Faridabad Sectors
            elif 28.35 <= latitude <= 28.45 and 77.25 <= longitude <= 77.35:
                base_price = 7700.0  # Faridabad (₹5,500 * 1.4)
            else:
                base_price = 8400.0  # Default for other areas (₹6,000 * 1.4)
            
            # ADJUST PRICING BASED ON PROPERTY FEATURES
            price_multiplier = 1.0
            
            # 1. Property Type Premium
            if type_of_building:
                building_type_upper = type_of_building.upper()
                if 'VILLA' in building_type_upper or 'BUNGALOW' in building_type_upper:
                    price_multiplier *= 1.35  # Villas are 35% more expensive
                elif 'PENTHOUSE' in building_type_upper:
                    price_multiplier *= 1.50  # Penthouses are 50% more expensive
                elif 'DUPLEX' in building_type_upper:
                    price_multiplier *= 1.20  # Duplexes are 20% more expensive
                elif 'STUDIO' in building_type_upper:
                    price_multiplier *= 0.85  # Studios are 15% cheaper
            
            # 2. Furnished Status Premium
            if furnished_status:
                furnished_upper = furnished_status.upper()
                if 'FURNISHED' in furnished_upper and 'SEMI' not in furnished_upper and 'UN' not in furnished_upper:
                    price_multiplier *= 1.15  # Fully furnished 15% premium
                elif 'SEMI' in furnished_upper:
                    price_multiplier *= 1.08  # Semi-furnished 8% premium
            
            # 3. Property Age/Status Premium
            if neworold:
                age_upper = neworold.upper()
                if 'NEW' in age_upper or 'UNDER CONSTRUCTION' in age_upper:
                    price_multiplier *= 1.12  # New properties 12% premium
            
            if status:
                status_upper = status.upper()
                if 'READY' in status_upper and 'MOVE' in status_upper:
                    price_multiplier *= 1.05  # Ready to move 5% premium
            
            # 4. Parking Premium (important in metro cities)
            if parking and parking > 0:
                if parking >= 2:
                    price_multiplier *= 1.10  # 2+ parking spaces = 10% premium
                else:
                    price_multiplier *= 1.05  # 1 parking space = 5% premium
            
            # 5. Lift/Elevator Premium
            if lift and lift > 0:
                price_multiplier *= 1.08  # Having lift = 8% premium
            
            # 6. Balcony Premium
            if balcony and balcony >= 2:
                price_multiplier *= 1.06  # Multiple balconies = 6% premium
            elif balcony and balcony > 0:
                price_multiplier *= 1.03  # One balcony = 3% premium
            
            # 7. Bedroom/Bathroom Configuration Premium
            if bedrooms >= 4:
                price_multiplier *= 1.12  # 4+ BHK properties = 12% premium
            elif bedrooms >= 3:
                price_multiplier *= 1.05  # 3 BHK = 5% premium
            
            if bathrooms >= 3:
                price_multiplier *= 1.05  # 3+ bathrooms = 5% premium
            
            # Calculate final price per sqft with all adjustments
            price_sqft = base_price * price_multiplier
            
            # Cap the price_sqft to realistic values for 2025 market (₹4,000 to ₹35,000)
            price_sqft = max(4000.0, min(35000.0, price_sqft))
        
        # Create input dictionary with all required features
        input_dict = {
            'area': area,
            'latitude': latitude,
            'longitude': longitude,
            'Bedrooms': bedrooms,
            'Bathrooms': bathrooms,
            'Balcony': balcony,
            'Status': status,
            'neworold': neworold,
            'parking': parking,
            'Furnished_status': furnished_status,
            'Lift': lift,
            'type_of_building': type_of_building,
            'Price_sqft': price_sqft,
            # Engineered features
            'total_rooms': bedrooms + bathrooms,
            'bed_bath_ratio': bedrooms / (bathrooms + 1),
            'has_parking': 1 if parking > 0 else 0,
            'has_lift': 1 if lift > 0 else 0,
            'has_balcony': 1 if balcony > 0 else 0
        }
        
        # Make prediction
        prediction = self.predict(input_dict)
        
        return prediction[0]
    
    def predict_batch(self, input_file, output_file='predictions.csv'):
        """
        Make predictions on a batch of houses from a CSV file.
        
        Parameters:
        -----------
        input_file : str
            Path to CSV file with input features
        output_file : str
            Path to save predictions
            
        Returns:
        --------
        pd.DataFrame : DataFrame with predictions
        """
        print(f"Loading data from: {input_file}")
        data = pd.read_csv(input_file)
        
        print("Making predictions...")
        predictions = self.predict(data)
        
        # Add predictions to dataframe
        data['predicted_price'] = predictions
        
        # Save to CSV
        data.to_csv(output_file, index=False)
        print(f"Predictions saved to: {output_file}")
        
        return data


def predict_price(model_path='house_price_model.pkl', **kwargs):
    """
    Convenience function to quickly predict a house price.
    
    Parameters:
    -----------
    model_path : str
        Path to the saved model
    **kwargs : dict
        House features (area, latitude, longitude, bedrooms, bathrooms, etc.)
        
    Returns:
    --------
    float : Predicted price
    """
    predictor = HousePricePredictor(model_path=model_path)
    prediction = predictor.predict_single(**kwargs)
    return prediction


def format_price(price):
    """
    Format price in Indian Rupee format.
    
    Parameters:
    -----------
    price : float
        Price to format
        
    Returns:
    --------
    str : Formatted price string
    """
    if price >= 10000000:  # 1 Crore
        return f"₹{price/10000000:.2f} Crore"
    elif price >= 100000:  # 1 Lakh
        return f"₹{price/100000:.2f} Lakh"
    else:
        return f"₹{price:,.2f}"


if __name__ == "__main__":
    """
    Example usage of the prediction module.
    """
    print("="*80)
    print("  HOUSE PRICE PREDICTION SYSTEM")
    print("="*80)
    
    # Initialize predictor
    try:
        predictor = HousePricePredictor(model_path='house_price_model.pkl')
        
        print("\n" + "="*80)
        print("  EXAMPLE PREDICTION")
        print("="*80)
        
        # Example prediction - 3 BHK apartment in Noida
        predicted_price = predictor.predict_single(
            area=1350.0,              # Square feet
            latitude=28.60885,        # Noida coordinates
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
        
        print("\nInput Features:")
        print(f"  Area: 1350 sq ft")
        print(f"  Location: Noida (Lat: 28.61, Long: 77.46)")
        print(f"  Configuration: 3 BHK, 3 Bathrooms")
        print(f"  Status: Ready to Move")
        print(f"  Type: New Property Flat")
        print(f"  Amenities: 2 Balconies, 1 Parking, 2 Lifts")
        print(f"  Furnished: Semi-Furnished")
        
        print(f"\n{'='*80}")
        print(f"  PREDICTED PRICE: {format_price(predicted_price)}")
        print(f"  (₹{predicted_price:,.2f})")
        print(f"{'='*80}")
        
        # Another example - 2 BHK apartment
        print("\n" + "="*80)
        print("  ANOTHER EXAMPLE PREDICTION")
        print("="*80)
        
        predicted_price_2 = predictor.predict_single(
            area=1000.0,
            latitude=28.52,
            longitude=77.35,
            bedrooms=2.0,
            bathrooms=2.0,
            balcony=1.0,
            status='Ready to Move',
            neworold='Resale',
            parking=1.0,
            type_of_building='Flat'
        )
        
        print("\nInput Features:")
        print(f"  Area: 1000 sq ft")
        print(f"  Location: Delhi NCR (Lat: 28.52, Long: 77.35)")
        print(f"  Configuration: 2 BHK, 2 Bathrooms")
        print(f"  Status: Ready to Move (Resale)")
        print(f"  Type: Flat")
        
        print(f"\n{'='*80}")
        print(f"  PREDICTED PRICE: {format_price(predicted_price_2)}")
        print(f"  (₹{predicted_price_2:,.2f})")
        print(f"{'='*80}\n")
        
    except FileNotFoundError:
        print("\n⚠️  ERROR: Model file not found!")
        print("Please train the model first by running: python model_training.py")
        print("="*80 + "\n")
    except Exception as e:
        print(f"\n⚠️  ERROR: {str(e)}")
        print("="*80 + "\n")
