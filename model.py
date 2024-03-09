import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.metrics import classification_report, accuracy_score
import joblib

def train_and_save_model():
    # Load the dataset
    df = pd.read_csv('combined_file.csv')

    # Define the target variable for each platform
    for platform in ['Netflix', 'PrimeVideo', 'Hotstar', 'Zee5']:
        df[f'Unenroll_{platform}'] = (df[f'{platform}_Watch_Time'] <= 5).astype(int)

    # Features and target variable
    features = ['Netflix_Watch_Time', 'PrimeVideo_Watch_Time', 'Hotstar_Watch_Time', 'Zee5_Watch_Time']
    target_platforms = ['Netflix', 'PrimeVideo', 'Hotstar', 'Zee5']

    # Train and evaluate models for each platform
    trained_models = {}
    for platform in target_platforms:
        # Features and target variable
        X = df[features]
        y = df[f'Unenroll_{platform}']

        # Split the dataset into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Create a pipeline to handle missing data and train the model
        model = make_pipeline(
            SimpleImputer(strategy='mean'),  # You can choose an imputation strategy based on your data
            RandomForestClassifier(n_estimators=100, random_state=42)
        )
        model.fit(X_train, y_train)

        # Save the trained model
        joblib.dump(model, f'{platform}_model.joblib')

        # Evaluate the model
        predictions = model.predict(X_test)
        print(f"\nClassification Report for {platform}:\n", classification_report(y_test, predictions))
        accuracy = accuracy_score(y_test, predictions)
        print(f"Accuracy for {platform}: {accuracy * 100:.2f}%")

        trained_models[platform] = model

        # Identify users to unenroll based on the trained model
        unenroll_users = df[df[f'Unenroll_{platform}'] == 1]['Username']
        for user in unenroll_users:
            print(f"User '{user}' needs to unenroll from {platform} due to low usage.")

    return trained_models

if __name__ == "__main__":
    # Train and save the models
    trained_models = train_and_save_model()
