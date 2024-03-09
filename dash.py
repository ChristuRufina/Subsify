import os
import streamlit as st
import pandas as pd
from joblib import load
import matplotlib.pyplot as plt
import seaborn as sns

# Load the trained models
netflix_model = load('Netflix_model.joblib')
primevideo_model = load('PrimeVideo_model.joblib')
hotstar_model = load('Hotstar_model.joblib')
zee5_model = load('Zee5_model.joblib')

# Mock user authentication function (replace with your authentication logic)
def authenticate_user(username, password):
    return username == password

def load_user_data(username):
    folder_path = 'Users'
    csv_filename = os.path.join(folder_path, f"{username}.csv")
    return pd.read_csv(csv_filename)

def main():
    st.title(" Subsify")

    # Login page
    st.header("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if authenticate_user(username, password):
            st.success("Login successful!")
            dashboard(username)
        else:
            st.error("Login failed. Please check your username and password.")

def dashboard(username):
    st.title(" 🎯 Subsify Dashboard")

    # Use the username to dynamically load the CSV file
    user_data = load_user_data(username)
    
    selected_user = st.selectbox("Select a user:", user_data['Username'].tolist())

    # Extract the selected user's watch time data
    selected_user_data = user_data[user_data['Username'] == selected_user][['Netflix_Watch_Time', 'PrimeVideo_Watch_Time', 'Hotstar_Watch_Time', 'Zee5_Watch_Time']]

    # Make predictions using the trained models
    netflix_prediction = netflix_model.predict(selected_user_data)[0]
    primevideo_prediction = primevideo_model.predict(selected_user_data)[0]
    hotstar_prediction = hotstar_model.predict(selected_user_data)[0]
    zee5_prediction = zee5_model.predict(selected_user_data)[0]

    # Display results
    st.subheader("Prediction Results")

    def display_churn_status(platform, prediction):
        if prediction == 1:
            st.write(f"{selected_user} should consider unenrolling from {platform}.")
        else:
            st.write(f"{selected_user} doesn't need to unenroll from {platform} based on watch time.")

    display_churn_status('Netflix', netflix_prediction)
    display_churn_status('Prime Video', primevideo_prediction)
    display_churn_status('Hotstar', hotstar_prediction)
    display_churn_status('Zee5', zee5_prediction)

    # Create a pie chart for platform usage
    usage_data = [selected_user_data.iloc[0]['Netflix_Watch_Time'],
                  selected_user_data.iloc[0]['PrimeVideo_Watch_Time'],
                  selected_user_data.iloc[0]['Hotstar_Watch_Time'],
                  selected_user_data.iloc[0]['Zee5_Watch_Time']]
    platforms = ['Netflix', 'Prime Video', 'Hotstar', 'Zee5']

    # Set a seaborn theme
    sns.set_theme()

    # Customize colors using a seaborn palette
    colors = sns.color_palette("pastel")

    # Plot the pie chart
    st.subheader("Platform Usage Distribution")
    fig, ax = plt.subplots()
    ax.pie(usage_data, labels=platforms, autopct='%1.1f%%', startangle=90, colors=colors)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(fig)

    # Create a bar graph for watch time distribution
    st.subheader("Watch Time Distribution Across Platforms")
    plt.figure(figsize=(10, 6))
    sns.barplot(x=platforms, y=usage_data, palette="pastel")
    plt.xlabel("Platforms")
    plt.ylabel("Watch Time")
    plt.title("Watch Time Distribution")
    plt.xticks(rotation=45)
    st.pyplot(plt)

# Run the Streamlit app
if __name__ == "__main__":
    main()
