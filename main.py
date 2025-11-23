"""
Main script to run the complete house price prediction pipeline.
This demonstrates the end-to-end workflow from data loading to prediction.
"""

from model_training import train_models
from predict import HousePricePredictor, format_price
from utils import print_section_header


def main():
    """
    Run the complete ML pipeline.
    """
    print("\n" + "="*80)
    print("  HOUSE PRICE PREDICTION - END-TO-END ML PIPELINE")
    print("="*80)
    
    # Step 1: Train models
    print("\nStarting model training pipeline...")
    print("This will:")
    print("  1. Load and explore the data")
    print("  2. Clean and preprocess the data")
    print("  3. Engineer new features")
    print("  4. Train multiple models (Linear Regression, Random Forest, XGBoost)")
    print("  5. Compare model performance")
    print("  6. Save the best model")
    print("\nThis may take a few minutes...\n")
    
    # Train models and save the best one
    best_model, best_model_name, all_models, results = train_models(
        data_path='Delhi_v2.csv',
        test_size=0.2,
        random_state=42,
        save_path='house_price_model.pkl'
    )
    
    # Step 2: Make example predictions
    print_section_header("Making Example Predictions")
    
    predictor = HousePricePredictor(model_path='house_price_model.pkl')
    
    # Example 1: Luxury 3 BHK in Noida
    print("\nExample 1: Luxury 3 BHK Apartment in Noida")
    print("-" * 80)
    predicted_price_1 = predictor.predict_single(
        area=1500.0,
        latitude=28.60885,
        longitude=77.46056,
        bedrooms=3.0,
        bathrooms=3.0,
        balcony=2.0,
        status='Ready to Move',
        neworold='New Property',
        parking=2.0,
        furnished_status='Furnished',
        lift=3.0,
        type_of_building='Flat'
    )
    print(f"Predicted Price: {format_price(predicted_price_1)} (₹{predicted_price_1:,.2f})")
    
    # Example 2: Budget 2 BHK
    print("\nExample 2: Budget 2 BHK Apartment")
    print("-" * 80)
    predicted_price_2 = predictor.predict_single(
        area=900.0,
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
    print(f"Predicted Price: {format_price(predicted_price_2)} (₹{predicted_price_2:,.2f})")
    
    # Example 3: Large 4 BHK
    print("\nExample 3: Spacious 4 BHK Apartment")
    print("-" * 80)
    predicted_price_3 = predictor.predict_single(
        area=2200.0,
        latitude=28.645,
        longitude=77.385,
        bedrooms=4.0,
        bathrooms=4.0,
        balcony=3.0,
        status='Ready to Move',
        neworold='New Property',
        parking=2.0,
        furnished_status='Semi-Furnished',
        lift=2.0,
        type_of_building='Flat'
    )
    print(f"Predicted Price: {format_price(predicted_price_3)} (₹{predicted_price_3:,.2f})")
    
    print("\n" + "="*80)
    print("  PIPELINE EXECUTION COMPLETED SUCCESSFULLY!")
    print("="*80)
    print("\nGenerated Files:")
    print("  ✓ house_price_model.pkl - Trained model")
    print("  ✓ random_forest_feature_importance.png - Feature importance plot")
    print("  ✓ xgboost_feature_importance.png - Feature importance plot (if XGBoost available)")
    print("  ✓ Prediction plots for best model")
    print("\nNext Steps:")
    print("  • Use predict.py to make new predictions")
    print("  • Load the model for deployment")
    print("  • Fine-tune hyperparameters for better performance")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
