import streamlit as st
from streamlit_option_menu import option_menu
import os
from dotenv import load_dotenv
import google.generativeai as gen_ai
import subprocess
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load environment variables
load_dotenv()

# Define the function to load user data from CSV
def load_user_data(username):
    folder_path = 'Users'
    csv_filename = os.path.join(folder_path, f"{username}.csv")
    try:
        return pd.read_csv(csv_filename)
    except FileNotFoundError:
        st.error(f"Error: CSV file '{csv_filename}' not found.")
        return None

# Define the function to authenticate user
def authenticate_user(username, password):
    # Check if the provided username and password are the same
    if username == password:
        return True
    else:
        return False

# Define the function to display churn status for each platform
def display_churn_status(platform, prediction, selected_user):
    if prediction == 1:
        st.write(f"{selected_user} should consider unenrolling from {platform}.")
    else:
        st.write(f"{selected_user} doesn't need to unenroll from {platform} based on watch time.")

# Define the function to display the dashboard
def dashboard(username):
    st.title("🎯 Subsify Dashboard")

    # Load user data
    user_data = load_user_data(username)
    if user_data is None:
        return

    selected_user = st.selectbox("Select a user:", user_data['Username'].tolist())

    # Extract the selected user's watch time data
    selected_user_data = user_data[user_data['Username'] == selected_user][['Netflix_Watch_Time', 'PrimeVideo_Watch_Time', 'Hotstar_Watch_Time', 'Zee5_Watch_Time']]

    # Display user data
    st.write(selected_user_data)

    # Make predictions using the trained models (Assuming predictions are available)
    netflix_prediction = 1  # Replace with actual prediction for Netflix
    primevideo_prediction = 0  # Replace with actual prediction for Prime Video
    hotstar_prediction = 1  # Replace with actual prediction for Hotstar
    zee5_prediction = 0  # Replace with actual prediction for Zee5

    # Display recommendations based on predictions
    st.subheader("Recommendations")
    display_churn_status('Netflix', netflix_prediction, selected_user)
    display_churn_status('Prime Video', primevideo_prediction, selected_user)
    display_churn_status('Hotstar', hotstar_prediction, selected_user)
    display_churn_status('Zee5', zee5_prediction, selected_user)
  
    # Create a pie chart for platform usage
    st.subheader("Platform Usage Distribution")
    fig, ax = plt.subplots()
    ax.pie(selected_user_data.iloc[0], labels=selected_user_data.columns, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(fig)

    # Create a bar chart for watch time distribution
    st.subheader("Watch Time Distribution Across Platforms")
    plt.figure(figsize=(10, 6))
    sns.barplot(data=selected_user_data, palette="pastel")
    plt.xlabel("Platforms")
    plt.ylabel("Watch Time")
    plt.title("Watch Time Distribution")
    plt.xticks(rotation=45)
    st.pyplot(plt)

# Set the background color of the page
st.markdown(
    """
    <style>
    body {
        background-color: #c7ecee; /* Use a cool tone color code */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Display the menu section with centered alignment
with st.markdown(
    """
    <div style="display: flex; justify-content: center;">
    """
):
    selected = option_menu(
        menu_title="Menu",
        options=["Home", "Dashboard", "Subsify-AI"],
        icons=["house", "bargraph", "envelope"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
    )

# Show the selected option
if selected == "Home":
    st.title(f"Welcome to {selected}")
    st.title("Welcome to Subsify!")
    st.image("pic1.png")
    st.write("""
        Subsify offers an all-encompassing solution for efficiently managing your subscription services. Whether you need to monitor your viewing habits, receive tailored recommendations, or organize your subscriptions seamlessly, Subsify is the ultimate tool for you!

Feel empowered to take charge of your entertainment journey with Subsify. Explore its array of features and unlock a world of convenience at your fingertips.
    """)
    st.write("Choose an option from the menu on the left to get started.")  
elif selected == "Dashboard":
    st.title(f"You have entered into  {selected}")
    # In the dashboard function, pass the username correctly
    username = st.text_input("Enter your username:")
    password = st.text_input("Enter your password:", type="password")
    if st.button("Login"):
        if authenticate_user(username, password):
            st.success("Login successful!")
            st.session_state.username = username
            dashboard(username)
        else:
            st.error("Login failed. Please check your username and password.")
elif selected == "Subsify-AI":
    st.title(f"Chat away with with our {selected}")
    # Set up Google Gemini-Pro AI model
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    gen_ai.configure(api_key=GOOGLE_API_KEY)
    model = gen_ai.GenerativeModel('gemini-pro')

    # Initialize chat session in Streamlit if not already present
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])

    # Display the chatbot's title on the page
    st.title("🤖 Subsify Pro - ChatBot")

    # Display the greeting message line by line
    st.write("Hello there! I'm Subsify-Pro, your personal assistant.")
    st.write("Feel free to ask me anything related to movie recommendations.")
    st.write("Tips to reduce screen time.")

    # Set background image using HTML/CSS
    page_bg_img = '''
    <style>
    body {
        background-image: url("https://images.unsplash.com/photo-1542281286-9e0a16bb7366");
        background-size: cover;
    }
    </style>
    '''

    st.markdown(page_bg_img, unsafe_allow_html=True)

    # Display the chat history
    for message in st.session_state.chat_session.history:
        with st.chat_message(message.role):
            st.markdown(message.parts[0].text)

    # Input field for user's message
    user_prompt = st.text_input("Ask Subsify-Pro...")
    if user_prompt:
        # Add user's message to chat and display it
        st.chat_message("user").markdown(user_prompt)

        # Send user's message to Gemini-Pro and get the response
        gemini_response = st.session_state.chat_session.send_message(user_prompt)

        # Display Gemini-Pro's response
        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)
