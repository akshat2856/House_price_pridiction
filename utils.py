"""
Utility functions for the house price prediction pipeline.
This module contains helper functions for evaluation, visualization, and saving models.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import joblib
import os


def evaluate_model(model, X_train, y_train, X_test, y_test, model_name="Model"):
    """
    Evaluate a regression model and print performance metrics.
    
    Parameters:
    -----------
    model : sklearn estimator
        Trained model to evaluate
    X_train : array-like
        Training features
    y_train : array-like
        Training target
    X_test : array-like
        Test features
    y_test : array-like
        Test target
    model_name : str
        Name of the model for display
        
    Returns:
    --------
    dict : Dictionary containing all metrics
    """
    # Make predictions
    train_pred = model.predict(X_train)
    test_pred = model.predict(X_test)
    
    # Calculate metrics for training set
    train_rmse = np.sqrt(mean_squared_error(y_train, train_pred))
    train_r2 = r2_score(y_train, train_pred)
    train_mae = mean_absolute_error(y_train, train_pred)
    
    # Calculate metrics for test set
    test_rmse = np.sqrt(mean_squared_error(y_test, test_pred))
    test_r2 = r2_score(y_test, test_pred)
    test_mae = mean_absolute_error(y_test, test_pred)
    
    # Print results
    print(f"\n{'='*60}")
    print(f"{model_name} Performance")
    print(f"{'='*60}")
    print(f"Training Set:")
    print(f"  RMSE: ₹{train_rmse:,.2f}")
    print(f"  MAE:  ₹{train_mae:,.2f}")
    print(f"  R²:   {train_r2:.4f}")
    print(f"\nTest Set:")
    print(f"  RMSE: ₹{test_rmse:,.2f}")
    print(f"  MAE:  ₹{test_mae:,.2f}")
    print(f"  R²:   {test_r2:.4f}")
    print(f"{'='*60}\n")
    
    return {
        'model_name': model_name,
        'train_rmse': train_rmse,
        'train_r2': train_r2,
        'train_mae': train_mae,
        'test_rmse': test_rmse,
        'test_r2': test_r2,
        'test_mae': test_mae
    }


def plot_feature_importance(model, feature_names, top_n=20, save_path='feature_importance.png'):
    """
    Plot feature importance for tree-based models.
    
    Parameters:
    -----------
    model : sklearn estimator
        Trained tree-based model with feature_importances_ attribute
    feature_names : list
        List of feature names
    top_n : int
        Number of top features to display
    save_path : str
        Path to save the plot
    """
    # Check if model has feature_importances_
    if not hasattr(model, 'feature_importances_'):
        print(f"Model {type(model).__name__} does not have feature_importances_ attribute")
        return
    
    # Get feature importances
    importances = model.feature_importances_
    
    # Create dataframe
    feature_importance_df = pd.DataFrame({
        'feature': feature_names,
        'importance': importances
    }).sort_values('importance', ascending=False).head(top_n)
    
    # Create plot
    plt.figure(figsize=(10, 8))
    sns.barplot(data=feature_importance_df, x='importance', y='feature', palette='viridis')
    plt.title(f'Top {top_n} Feature Importances', fontsize=16, fontweight='bold')
    plt.xlabel('Importance', fontsize=12)
    plt.ylabel('Feature', fontsize=12)
    plt.tight_layout()
    
    # Save plot
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Feature importance plot saved to: {save_path}")
    plt.close()
    
    return feature_importance_df


def plot_predictions(y_true, y_pred, model_name="Model", save_path='predictions_plot.png'):
    """
    Plot actual vs predicted values.
    
    Parameters:
    -----------
    y_true : array-like
        Actual target values
    y_pred : array-like
        Predicted target values
    model_name : str
        Name of the model for the plot title
    save_path : str
        Path to save the plot
    """
    plt.figure(figsize=(10, 6))
    plt.scatter(y_true, y_pred, alpha=0.5, edgecolors='k', linewidths=0.5)
    
    # Plot perfect prediction line
    min_val = min(y_true.min(), y_pred.min())
    max_val = max(y_true.max(), y_pred.max())
    plt.plot([min_val, max_val], [min_val, max_val], 'r--', lw=2, label='Perfect Prediction')
    
    plt.xlabel('Actual Price (₹)', fontsize=12)
    plt.ylabel('Predicted Price (₹)', fontsize=12)
    plt.title(f'{model_name}: Actual vs Predicted Prices', fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Save plot
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Predictions plot saved to: {save_path}")
    plt.close()


def save_model(model, filepath='house_price_model.pkl'):
    """
    Save a trained model to disk using joblib.
    
    Parameters:
    -----------
    model : sklearn estimator
        Trained model to save
    filepath : str
        Path where the model will be saved
    """
    joblib.dump(model, filepath)
    print(f"Model saved successfully to: {filepath}")


def load_model(filepath='house_price_model.pkl'):
    """
    Load a saved model from disk.
    
    Parameters:
    -----------
    filepath : str
        Path to the saved model
        
    Returns:
    --------
    sklearn estimator : Loaded model
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Model file not found: {filepath}")
    
    model = joblib.load(filepath)
    print(f"Model loaded successfully from: {filepath}")
    return model


def compare_models(results_list):
    """
    Create a comparison table for multiple models.
    
    Parameters:
    -----------
    results_list : list of dict
        List of result dictionaries from evaluate_model function
        
    Returns:
    --------
    pd.DataFrame : Comparison table
    """
    df = pd.DataFrame(results_list)
    df = df.sort_values('test_r2', ascending=False)
    
    print("\n" + "="*80)
    print("MODEL COMPARISON SUMMARY")
    print("="*80)
    print(df.to_string(index=False))
    print("="*80 + "\n")
    
    return df


def print_section_header(title):
    """
    Print a formatted section header.
    
    Parameters:
    -----------
    title : str
        Section title to display
    """
    print("\n" + "="*80)
    print(f"  {title.upper()}")
    print("="*80 + "\n")
