# Import necessary libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
import joblib

def train_model():
    # Load the dataset
    df = pd.read_csv("dataset.csv")

    # Define a popularity threshold based on the median
    threshold = df["Popularity_Score"].median()
    df["Popularity Label"] = np.where(df["Popularity_Score"] >= threshold, 1, 0)

    # Select features and target
    X = df[["Year_of_Release", "Developer", "Genre", "YouTube_Likes", "Twitter_Followers"]]
    y = df["Popularity Label"]

    # Preprocessing pipeline
    numeric_features = ["Year_of_Release", "YouTube_Likes", "Twitter_Followers"]
    categorical_features = ["Developer", "Genre"]

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric_features),
            ("cat", OneHotEncoder(), categorical_features)
        ]
    )

    # Create pipeline
    pipeline = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("classifier", SVC(random_state=42))
    ])

    # Split and train
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    pipeline.fit(X_train, y_train)
    # Save the model
    joblib.dump(pipeline, 'game_popularity_model.joblib')
    return pipeline
    

def predict_popularity(game_name, year_of_release, developer, genre, youtube_likes, twitter_followers):
    try:
        # Load the model
        pipeline = joblib.load('game_popularity_model.joblib')
        
        # Create input DataFrame
        new_data = pd.DataFrame({
            "Year_of_Release": [year_of_release],
            "Developer": [developer],
            "Genre": [genre],
            "YouTube_Likes": [youtube_likes],
            "Twitter_Followers": [twitter_followers]
        })
        
        # Make prediction
        popularity_label = pipeline.predict(new_data)[0]
        
        if popularity_label == 1:
            return f"The game '{game_name}' is predicted to have HIGH popularity."
        else:
            return f"The game '{game_name}' is predicted to have LOW popularity."
    except Exception as e:
        return f"Error making prediction: {str(e)}"

# Train the model when this file is run directly
if __name__ == "__main__":
    train_model()
