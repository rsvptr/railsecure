# utils/helpers.py
# This module contains utility functions shared across the RailSecure Learning Platform.
# These include API client initializations, UI helper functions (like setting background),
# session state management, and formatting helpers for API calls.

import streamlit as st
from openai import OpenAI # OpenAI Python library for GPT interaction
import os               # Standard library for interacting with the operating system (e.g., path checks)
import base64           # Standard library for encoding binary data to text (used for local images)
from datetime import datetime # Standard library for date and time operations

# ---------------------------------------------------
# OpenAI Client Initialization
# ---------------------------------------------------
def get_openai_client():
    """
    Initializes and returns an OpenAI client instance.

    Retrieves the OpenAI API key from Streamlit's secrets management.
    If the key is not found or is invalid, an error message is displayed
    in the Streamlit app, and None is returned.

    Returns:
        openai.OpenAI or None: An initialized OpenAI client if successful, otherwise None.
    """
    try:
        # Attempt to retrieve the API key from st.secrets
        api_key = st.secrets["OPENAI_API_KEY"]
        if not api_key: # Check if the key is empty
            st.error("OpenAI API key is not set in Streamlit secrets. Please add it to your secrets.toml file.")
            return None
        # Return an initialized OpenAI client
        return OpenAI(api_key=api_key)
    except KeyError:
        # Handle cases where the key name is not found in secrets
        st.error("OpenAI API key (OPENAI_API_KEY) not found in Streamlit secrets. Please ensure it's correctly configured in .streamlit/secrets.toml.")
        return None
    except Exception as e:
        # Handle any other exceptions during client initialization
        st.error(f"An error occurred while initializing the OpenAI client: {e}")
        return None

# ---------------------------------------------------
# NVD API Key Retrieval (Optional)
# ---------------------------------------------------
def get_nvd_api_key():
    """
    Retrieves the NVD (National Vulnerability Database) API key from Streamlit secrets, if available.
    Using an NVD API key can provide higher rate limits for API requests.

    Returns:
        str or None: The NVD API key if found and configured, otherwise None.
    """
    try:
        # Use .get() for safer retrieval; returns None if the key doesn't exist
        return st.secrets.get("NVD_API_KEY")
    except Exception: # Catch any other potential issues with secrets access
        # This is less likely with .get() but good for robustness
        return None

# ---------------------------------------------------
# Function to set a background image for the Streamlit app
# Attempts to load ONLY from a local file.
# ---------------------------------------------------
def get_local_image_as_base64(path):
    """
    Reads a local image file and returns it as a base64 encoded string.
    This allows embedding the image directly into CSS.

    Args:
        path (str): The file path to the local image.

    Returns:
        str or None: A base64 data URI string if successful, otherwise None.
                     Displays an error in Streamlit if the file is not found or unreadable.
    """
    if not os.path.exists(path):
        # Display an error if the image file doesn't exist at the specified path
        st.error(
            f"Required background image not found at '{path}'. "
            "Please ensure the image exists in the correct location."
        )
        return None
    try:
        # Open the image file in binary read mode
        with open(path, "rb") as image_file:
            # Read the file content and encode it to base64
            encoded_string = base64.b64encode(image_file.read()).decode()
        
        # Determine the image type from the file extension for the data URI
        image_type = path.split('.')[-1].lower()
        if image_type == "jpg":
            image_type = "jpeg" # Standard MIME type for JPEG
        
        # Return the base64 string formatted as a data URI
        return f"data:image/{image_type};base64,{encoded_string}"
    except Exception as e:
        # Display an error if any issue occurs during file reading or encoding
        st.error(f"Could not read or encode local background image '{path}': {e}")
        return None

def set_app_background():
    """
    Applies a custom background image and base styling to the Streamlit application.

    It attempts to load a background image from 'assets/background.jpg'.
    If the local image is not found or fails to load, no custom background image is applied,
    and a warning is displayed.
    CSS for text readability and UI element styling is applied regardless of
    the background image's success.
    """
    local_image_path = "assets/background.jpg" # Path to the local background image
    
    background_source_css = "" # Initialize CSS string for the background image
    background_data = get_local_image_as_base64(local_image_path) # Attempt to load the image
    
    if background_data:
        # If image data is loaded, construct the CSS for the background
        background_source_css = f"""
        .stApp {{
            background-image: url("{background_data}");
            background-attachment: fixed; /* Keeps background fixed during scroll */
            background-size: cover;       /* Ensures background covers the entire area */
        }}
        """
    else:
        # If image loading fails, display a warning
        # get_local_image_as_base64() would have already shown an st.error for file not found.
        st.warning(
            "Application background image could not be loaded. "
            "The app will continue without a custom background image."
        )

    # Apply CSS for text readability and other UI elements
    # This CSS is applied whether the background image loaded or not,
    # to maintain a consistent look, especially for dark themes.
    st.markdown(
        f"""
        <style>
        {background_source_css} /* Injects background CSS if available, otherwise empty */

        /* General text and app background color adjustments for readability */
        body, .stApp, .stMarkdown, 
        .stTextInput > div > div > input, 
        .stTextArea > div > div > textarea, 
        .stSelectbox > div > div > div {{
            color: #E0E0E0; /* Light grey for text on dark backgrounds */
        }}
        /* Button styling */
        .stButton > button {{
            border: 1px solid #E0E0E0;
            color: #E0E0E0; 
        }}
        .stButton > button:hover {{
            border: 1px solid #FFFFFF;
            color: #FFFFFF; 
        }}

        /* Header styling */
        h1, h2, h3, h4, h5, h6 {{
            color: #FFFFFF; /* White for headers */
        }}
        
        /* Custom styling for Streamlit's alert boxes (info, warning, error, success) */
        .stAlert[data-baseweb="alert"] div[role="alert"] {{ /* Base for info */
            background-color: rgba(0, 100, 255, 0.25); 
            color: #E0E0E0; 
            border-radius: 0.5rem;
        }}
        .stAlert[data-baseweb="alert"][class*="stWarning"] div[role="alert"] {{ /* For warning */
            background-color: rgba(255, 165, 0, 0.25); 
            color: #E0E0E0;
            border-radius: 0.5rem;
        }}
        .stAlert[data-baseweb="alert"][class*="stError"] div[role="alert"] {{ /* For error */
            background-color: rgba(255, 0, 0, 0.25); 
            color: #E0E0E0;
            border-radius: 0.5rem;
        }}
        .stAlert[data-baseweb="alert"][class*="stSuccess"] div[role="alert"] {{ /* For success */
            background-color: rgba(0, 128, 0, 0.25);
            color: #E0E0E0;
            border-radius: 0.5rem;
        }}
        </style>
        """,
        unsafe_allow_html=True, # Allows Streamlit to render the HTML and CSS
    )

# ---------------------------------------------------
# Initialize session state for storing persistent values
# ---------------------------------------------------
def init_session_state():
    """
    Initializes Streamlit session state variables if they are not already present.
    This ensures that necessary keys exist in `st.session_state` across app reruns
    and user interactions, preventing KeyErrors.

    The `defaults` dictionary defines all session state keys used by the application
    and their initial values.
    """
    defaults = {
        # Phishing Module
        "phishing_email_content": None, # Stores generated phishing email text
        "phishing_evaluation": None,    # Stores feedback on user's phishing explanation
        "pasted_email_analysis": None,  # Stores analysis of user-pasted email

        # Scenario Quiz Module
        "current_scenario_text": None,  # Stores generated incident scenario text
        "scenario_evaluation": None,    # Stores feedback on user's scenario response

        # Cybersecurity Quiz Module
        "parsed_quiz_questions": None,      # Stores parsed quiz questions (list of dicts)
        "user_quiz_selections": {},       # Stores user's answers to the current quiz
        "quiz_evaluation_feedback": None, # Stores the feedback/results of the quiz

        # Password Generator Module
        "generated_password": None,             # Stores the generated password
        "generated_password_strength": None,    # Strength level of the generated password
        "generated_password_feedback": None,    # Feedback details for generated password strength

        # Incident Response Guide Module
        "custom_incident_guide": None,  # Stores generated custom incident response guide

        # Compliance Hub & Reference Modules (for AI Q&A)
        "compliance_query_answer": None,# Stores AI response for compliance queries
        "reference_query_answer": None, # Stores AI response for reference material queries
        
        # Note: 'current_quiz_questions' was in original, replaced by 'parsed_quiz_questions'
        # 'quiz_evaluation' was in original, replaced by 'quiz_evaluation_feedback'
        # 'user_quiz_answers' (from old quiz) is now handled by 'user_quiz_selections'
    }
    # Iterate through the defaults and initialize if key is not in session_state
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# ---------------------------------------------------
# Helper function to create LLM message structure
# ---------------------------------------------------
def create_llm_messages(system_prompt, user_prompt):
    """
    Creates a standard message list structure for OpenAI Chat Completions API.
    The Chat Completions API expects a list of message objects, each with 'role' and 'content'.

    Args:
        system_prompt (str): The system message to guide the AI's behavior.
        user_prompt (str): The user's message or query.

    Returns:
        list: A list of message dictionaries formatted for the OpenAI API.
    """
    return [
        {"role": "system", "content": system_prompt}, # System message sets the context for the AI
        {"role": "user", "content": user_prompt}      # User message provides the specific input
    ]
