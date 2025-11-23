"""
Model training module for house price prediction.
Trains multiple regression models and compares their performance.
"""

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
import warnings
warnings.filterwarnings('ignore')

# Import utils
from utils import (
    evaluate_model, 
    plot_feature_importance, 
    plot_predictions,
    save_model, 
    compare_models,
    print_section_header
)

# Import preprocessing
from data_preprocessing import preprocess_data

# Try to import XGBoost, but handle gracefully if not available
try:
    from xgboost import XGBRegressor
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False
    print("Warning: XGBoost not available. Will skip XGBoost model.")


class ModelTrainer:
    """
    Handles training and evaluation of multiple regression models.
    """
    
    def __init__(self, X_train, X_test, y_train, y_test, preprocessor, feature_names, random_state=42):
        """
        Initialize the model trainer.
        
        Parameters:
        -----------
        X_train : pd.DataFrame
            Training features
        X_test : pd.DataFrame
            Test features
        y_train : pd.Series
            Training target
        y_test : pd.Series
            Test target
        preprocessor : ColumnTransformer
            Fitted preprocessing pipeline
        feature_names : list
            List of feature names after preprocessing
        random_state : int
            Random seed for reproducibility
        """
        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test
        self.preprocessor = preprocessor
        self.feature_names = feature_names
        self.random_state = random_state
        self.models = {}
        self.results = []
        self.best_model = None
        self.best_model_name = None
        
    def train_linear_regression(self):
        """
        Train a Linear Regression model.
        
        Returns:
        --------
        Pipeline : Trained Linear Regression pipeline
        """
        print_section_header("Training Linear Regression Model")
        
        # Create pipeline with preprocessor and model
        lr_pipeline = Pipeline(steps=[
            ('preprocessor', self.preprocessor),
            ('regressor', LinearRegression())
        ])
        
        # Train the model
        lr_pipeline.fit(self.X_train, self.y_train)
        
        # Evaluate the model
        # For evaluation, we need the preprocessed data
        X_train_processed = self.preprocessor.transform(self.X_train)
        X_test_processed = self.preprocessor.transform(self.X_test)
        
        results = evaluate_model(
            lr_pipeline.named_steps['regressor'],
            X_train_processed,
            self.y_train,
            X_test_processed,
            self.y_test,
            model_name="Linear Regression"
        )
        
        self.models['Linear Regression'] = lr_pipeline
        self.results.append(results)
        
        return lr_pipeline
    
    def train_random_forest(self, n_estimators=100, max_depth=20, min_samples_split=5):
        """
        Train a Random Forest Regressor model.
        
        Parameters:
        -----------
        n_estimators : int
            Number of trees in the forest
        max_depth : int
            Maximum depth of the trees
        min_samples_split : int
            Minimum samples required to split a node
            
        Returns:
        --------
        Pipeline : Trained Random Forest pipeline
        """
        print_section_header("Training Random Forest Regressor")
        
        # Create pipeline with preprocessor and model
        rf_pipeline = Pipeline(steps=[
            ('preprocessor', self.preprocessor),
            ('regressor', RandomForestRegressor(
                n_estimators=n_estimators,
                max_depth=max_depth,
                min_samples_split=min_samples_split,
                random_state=self.random_state,
                n_jobs=-1,  # Use all CPU cores
                verbose=0
            ))
        ])
        
        # Train the model
        print("Training Random Forest... This may take a few moments.")
        rf_pipeline.fit(self.X_train, self.y_train)
        
        # Evaluate the model
        X_train_processed = self.preprocessor.transform(self.X_train)
        X_test_processed = self.preprocessor.transform(self.X_test)
        
        results = evaluate_model(
            rf_pipeline.named_steps['regressor'],
            X_train_processed,
            self.y_train,
            X_test_processed,
            self.y_test,
            model_name="Random Forest"
        )
        
        self.models['Random Forest'] = rf_pipeline
        self.results.append(results)
        
        # Plot feature importance
        plot_feature_importance(
            rf_pipeline.named_steps['regressor'],
            self.feature_names,
            top_n=20,
            save_path='random_forest_feature_importance.png'
        )
        
        return rf_pipeline
    
    def train_xgboost(self, n_estimators=100, max_depth=6, learning_rate=0.1):
        """
        Train an XGBoost Regressor model.
        
        Parameters:
        -----------
        n_estimators : int
            Number of boosting rounds
        max_depth : int
            Maximum depth of the trees
        learning_rate : float
            Learning rate for boosting
            
        Returns:
        --------
        Pipeline : Trained XGBoost pipeline or None if XGBoost not available
        """
        if not XGBOOST_AVAILABLE:
            print("XGBoost is not available. Skipping XGBoost training.")
            return None
        
        print_section_header("Training XGBoost Regressor")
        
        # Create pipeline with preprocessor and model
        xgb_pipeline = Pipeline(steps=[
            ('preprocessor', self.preprocessor),
            ('regressor', XGBRegressor(
                n_estimators=n_estimators,
                max_depth=max_depth,
                learning_rate=learning_rate,
                random_state=self.random_state,
                n_jobs=-1,
                verbosity=0
            ))
        ])
        
        # Train the model
        print("Training XGBoost... This may take a few moments.")
        xgb_pipeline.fit(self.X_train, self.y_train)
        
        # Evaluate the model
        X_train_processed = self.preprocessor.transform(self.X_train)
        X_test_processed = self.preprocessor.transform(self.X_test)
        
        results = evaluate_model(
            xgb_pipeline.named_steps['regressor'],
            X_train_processed,
            self.y_train,
            X_test_processed,
            self.y_test,
            model_name="XGBoost"
        )
        
        self.models['XGBoost'] = xgb_pipeline
        self.results.append(results)
        
        # Plot feature importance
        plot_feature_importance(
            xgb_pipeline.named_steps['regressor'],
            self.feature_names,
            top_n=20,
            save_path='xgboost_feature_importance.png'
        )
        
        return xgb_pipeline
    
    def train_all_models(self):
        """
        Train all available models.
        
        Returns:
        --------
        dict : Dictionary of all trained models
        """
        print_section_header("Starting Model Training Pipeline")
        
        # Train Linear Regression
        self.train_linear_regression()
        
        # Train Random Forest
        self.train_random_forest(n_estimators=100, max_depth=20, min_samples_split=5)
        
        # Train XGBoost (if available)
        if XGBOOST_AVAILABLE:
            self.train_xgboost(n_estimators=100, max_depth=6, learning_rate=0.1)
        
        return self.models
    
    def compare_and_select_best(self):
        """
        Compare all models and select the best one based on test R² score.
        
        Returns:
        --------
        tuple : (best_model, best_model_name)
        """
        print_section_header("Comparing Model Performance")
        
        # Compare models
        comparison_df = compare_models(self.results)
        
        # Select best model based on test R² score
        best_result = max(self.results, key=lambda x: x['test_r2'])
        self.best_model_name = best_result['model_name']
        self.best_model = self.models[self.best_model_name]
        
        print(f"\n🏆 Best Model: {self.best_model_name}")
        print(f"   Test R² Score: {best_result['test_r2']:.4f}")
        print(f"   Test RMSE: ₹{best_result['test_rmse']:,.2f}")
        
        # Plot predictions for best model
        X_test_processed = self.preprocessor.transform(self.X_test)
        y_pred = self.best_model.named_steps['regressor'].predict(X_test_processed)
        
        plot_predictions(
            self.y_test,
            y_pred,
            model_name=self.best_model_name,
            save_path=f'{self.best_model_name.lower().replace(" ", "_")}_predictions.png'
        )
        
        return self.best_model, self.best_model_name
    
    def save_best_model(self, filepath='house_price_model.pkl'):
        """
        Save the best model to disk.
        
        Parameters:
        -----------
        filepath : str
            Path where the model will be saved
        """
        if self.best_model is None:
            raise ValueError("No best model selected. Call compare_and_select_best first.")
        
        print_section_header("Saving Best Model")
        save_model(self.best_model, filepath)
        print(f"Best model ({self.best_model_name}) saved to: {filepath}")


def train_models(data_path='Delhi_v2.csv', test_size=0.2, random_state=42, 
                save_path='house_price_model.pkl'):
    """
    Complete model training pipeline - convenience function.
    
    Parameters:
    -----------
    data_path : str
        Path to the CSV file
    test_size : float
        Proportion of data to use for testing
    random_state : int
        Random seed for reproducibility
    save_path : str
        Path to save the best model
        
    Returns:
    --------
    tuple : (best_model, best_model_name, all_models, results)
    """
    # Step 1: Preprocess data
    print_section_header("Data Preprocessing Phase")
    X_train, X_test, y_train, y_test, preprocessor, feature_names = preprocess_data(
        data_path=data_path,
        test_size=test_size,
        random_state=random_state
    )
    
    # Step 2: Initialize trainer
    trainer = ModelTrainer(
        X_train, X_test, y_train, y_test,
        preprocessor, feature_names, random_state
    )
    
    # Step 3: Train all models
    all_models = trainer.train_all_models()
    
    # Step 4: Compare and select best model
    best_model, best_model_name = trainer.compare_and_select_best()
    
    # Step 5: Save best model
    trainer.save_best_model(filepath=save_path)
    
    print_section_header("Model Training Pipeline Completed Successfully!")
    
    return best_model, best_model_name, all_models, trainer.results


if __name__ == "__main__":
    # Run the complete training pipeline
    best_model, best_model_name, all_models, results = train_models(
        data_path='Delhi_v2.csv',
        test_size=0.2,
        random_state=42,
        save_path='house_price_model.pkl'
    )
    
    print("\n" + "="*80)
    print("TRAINING COMPLETE!")
    print(f"Best model: {best_model_name}")
    print(f"Model saved as: house_price_model.pkl")
    print("="*80)
