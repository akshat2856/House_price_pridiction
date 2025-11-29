"""
Data preprocessing module for house price prediction.
Handles data loading, cleaning, feature engineering, and transformation.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer


class HousePricePreprocessor:
    """
    Handles all data preprocessing tasks for house price prediction.
    Includes missing value handling, feature engineering, and encoding.
    """
    
    def __init__(self, data_path='Delhi_v2.csv', target_column='price', random_state=42):
        """
        Initialize the preprocessor.
        
        Parameters:
        -----------
        data_path : str
            Path to the CSV file
        target_column : str
            Name of the target variable column
        random_state : int
            Random seed for reproducibility
        """
        self.data_path = data_path
        self.target_column = target_column
        self.random_state = random_state
        self.df = None
        self.preprocessor = None
        self.feature_names = None
        
    def load_data(self):
        """
        Load the dataset from CSV file and apply price inflation adjustment.
        
        Returns:
        --------
        pd.DataFrame : Loaded dataset with adjusted prices
        """
        print("Loading dataset...")
        self.df = pd.read_csv(self.data_path)
        
        # Apply 1.4x price inflation adjustment (4-year appreciation)
        if 'price' in self.df.columns:
            print("\n🔄 Applying price inflation adjustment (1.4x for 4-year appreciation)...")
            original_mean_price = self.df['price'].mean()
            self.df['price'] = self.df['price'] * 1.4
            
            # Also adjust Price_sqft if it exists
            if 'Price_sqft' in self.df.columns:
                self.df['Price_sqft'] = self.df['Price_sqft'] * 1.4
            
            adjusted_mean_price = self.df['price'].mean()
            print(f"   Original average price: ₹{original_mean_price/100000:.2f} Lac")
            print(f"   Adjusted average price: ₹{adjusted_mean_price/100000:.2f} Lac")
            print(f"   ✅ Prices increased by 40% to reflect current market rates")
        
        print(f"\nDataset loaded successfully!")
        print(f"Shape: {self.df.shape}")
        print(f"\nFirst few rows:")
        print(self.df.head())
        print(f"\nColumn names: {self.df.columns.tolist()}")
        print(f"\nMissing values:\n{self.df.isnull().sum()}")
        return self.df
    
    def clean_data(self):
        """
        Clean the dataset by handling missing values and removing irrelevant columns.
        
        Returns:
        --------
        pd.DataFrame : Cleaned dataset
        """
        print("\nCleaning data...")
        
        # Drop the unnamed index column if it exists
        if 'Unnamed: 0' in self.df.columns:
            self.df = self.df.drop('Unnamed: 0', axis=1)
        
        # Drop 'desc' column (long text descriptions are not useful for modeling)
        if 'desc' in self.df.columns:
            self.df = self.df.drop('desc', axis=1)
        
        # Drop 'Address' column (too specific, we have lat/long instead)
        if 'Address' in self.df.columns:
            self.df = self.df.drop('Address', axis=1)
        
        # Drop 'Landmarks' column (too many missing values and high cardinality)
        if 'Landmarks' in self.df.columns:
            self.df = self.df.drop('Landmarks', axis=1)
        
        # Remove rows where target variable (price) is missing
        if self.target_column in self.df.columns:
            self.df = self.df[self.df[self.target_column].notna()]
        
        # Remove outliers in price (very extreme values)
        # Keep prices between 1st and 99th percentile
        lower_bound = self.df[self.target_column].quantile(0.01)
        upper_bound = self.df[self.target_column].quantile(0.99)
        self.df = self.df[
            (self.df[self.target_column] >= lower_bound) & 
            (self.df[self.target_column] <= upper_bound)
        ]
        
        # Remove outliers in area
        if 'area' in self.df.columns:
            lower_area = self.df['area'].quantile(0.01)
            upper_area = self.df['area'].quantile(0.99)
            self.df = self.df[
                (self.df['area'] >= lower_area) & 
                (self.df['area'] <= upper_area)
            ]
        
        print(f"Data cleaned! New shape: {self.df.shape}")
        return self.df
    
    def engineer_features(self):
        """
        Create new features from existing ones.
        
        Returns:
        --------
        pd.DataFrame : Dataset with engineered features
        """
        print("\nEngineering features...")
        
        # Create price per sqft if not already present
        if 'area' in self.df.columns and 'price' in self.df.columns:
            if 'Price_sqft' not in self.df.columns:
                self.df['Price_sqft'] = self.df['price'] / self.df['area']
        
        # Create total rooms feature
        if 'Bedrooms' in self.df.columns and 'Bathrooms' in self.df.columns:
            self.df['total_rooms'] = self.df['Bedrooms'] + self.df['Bathrooms']
        
        # Create bedroom-bathroom ratio
        if 'Bedrooms' in self.df.columns and 'Bathrooms' in self.df.columns:
            self.df['bed_bath_ratio'] = self.df['Bedrooms'] / (self.df['Bathrooms'] + 1)
        
        # Binary feature: has parking
        if 'parking' in self.df.columns:
            self.df['has_parking'] = (self.df['parking'] > 0).astype(int)
        
        # Binary feature: has lift
        if 'Lift' in self.df.columns:
            self.df['has_lift'] = (self.df['Lift'] > 0).astype(int)
        
        # Binary feature: has balcony
        if 'Balcony' in self.df.columns:
            self.df['has_balcony'] = (self.df['Balcony'] > 0).astype(int)
        
        print("Feature engineering completed!")
        return self.df
    
    def prepare_data(self, test_size=0.2):
        """
        Prepare data for modeling: separate features and target, create train/test split.
        
        Parameters:
        -----------
        test_size : float
            Proportion of data to use for testing
            
        Returns:
        --------
        tuple : (X_train, X_test, y_train, y_test)
        """
        print("\nPreparing data for modeling...")
        
        # Separate features and target
        X = self.df.drop(self.target_column, axis=1)
        y = self.df[self.target_column]
        
        # Split data into train and test sets
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=self.random_state
        )
        
        print(f"Training set size: {X_train.shape}")
        print(f"Test set size: {X_test.shape}")
        
        return X_train, X_test, y_train, y_test
    
    def create_preprocessor(self, X):
        """
        Create a preprocessing pipeline using ColumnTransformer.
        Handles both numeric and categorical features.
        
        Parameters:
        -----------
        X : pd.DataFrame
            Feature dataframe
            
        Returns:
        --------
        ColumnTransformer : Preprocessing pipeline
        """
        print("\nCreating preprocessing pipeline...")
        
        # Identify numeric and categorical columns
        numeric_features = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
        categorical_features = X.select_dtypes(include=['object']).columns.tolist()
        
        print(f"Numeric features ({len(numeric_features)}): {numeric_features}")
        print(f"Categorical features ({len(categorical_features)}): {categorical_features}")
        
        # Create transformers for numeric features
        # Impute missing values with median, then scale
        numeric_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())
        ])
        
        # Create transformers for categorical features
        # Impute missing values with most frequent, then one-hot encode
        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='constant', fill_value='Unknown')),
            ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
        ])
        
        # Combine transformers using ColumnTransformer
        self.preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numeric_features),
                ('cat', categorical_transformer, categorical_features)
            ],
            remainder='drop'  # Drop any columns not specified
        )
        
        print("Preprocessing pipeline created successfully!")
        return self.preprocessor
    
    def get_feature_names(self, X):
        """
        Get feature names after preprocessing (including one-hot encoded features).
        
        Parameters:
        -----------
        X : pd.DataFrame
            Original feature dataframe
            
        Returns:
        --------
        list : Feature names after preprocessing
        """
        if self.preprocessor is None:
            raise ValueError("Preprocessor not created yet. Call create_preprocessor first.")
        
        # Get numeric feature names
        numeric_features = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
        
        # Get categorical feature names (after one-hot encoding)
        categorical_features = X.select_dtypes(include=['object']).columns.tolist()
        
        # Fit preprocessor to get encoded feature names
        self.preprocessor.fit(X)
        
        # Get one-hot encoded feature names
        cat_encoder = self.preprocessor.named_transformers_['cat']['onehot']
        cat_feature_names = cat_encoder.get_feature_names_out(categorical_features)
        
        # Combine all feature names
        self.feature_names = numeric_features + cat_feature_names.tolist()
        
        return self.feature_names
    
    def run_full_pipeline(self, test_size=0.2):
        """
        Run the complete preprocessing pipeline.
        
        Parameters:
        -----------
        test_size : float
            Proportion of data to use for testing
            
        Returns:
        --------
        tuple : (X_train, X_test, y_train, y_test, preprocessor, feature_names)
        """
        # Step 1: Load data
        self.load_data()
        
        # Step 2: Clean data
        self.clean_data()
        
        # Step 3: Engineer features
        self.engineer_features()
        
        # Step 4: Prepare data (split into train/test)
        X_train, X_test, y_train, y_test = self.prepare_data(test_size=test_size)
        
        # Step 5: Create preprocessor
        self.create_preprocessor(X_train)
        
        # Step 6: Get feature names
        self.get_feature_names(X_train)
        
        print("\n" + "="*80)
        print("PREPROCESSING PIPELINE COMPLETED SUCCESSFULLY!")
        print("="*80)
        
        return X_train, X_test, y_train, y_test, self.preprocessor, self.feature_names


# Standalone function for easy import
def preprocess_data(data_path='Delhi_v2.csv', test_size=0.2, random_state=42):
    """
    Convenience function to run the full preprocessing pipeline.
    
    Parameters:
    -----------
    data_path : str
        Path to the CSV file
    test_size : float
        Proportion of data to use for testing
    random_state : int
        Random seed for reproducibility
        
    Returns:
    --------
    tuple : (X_train, X_test, y_train, y_test, preprocessor, feature_names)
    """
    preprocessor_obj = HousePricePreprocessor(
        data_path=data_path,
        target_column='price',
        random_state=random_state
    )
    
    return preprocessor_obj.run_full_pipeline(test_size=test_size)


if __name__ == "__main__":
    # Example usage
    X_train, X_test, y_train, y_test, preprocessor, feature_names = preprocess_data()
    
    print(f"\nPreprocessing complete!")
    print(f"Number of features: {len(feature_names)}")
    print(f"Feature names: {feature_names[:10]}... (showing first 10)")
