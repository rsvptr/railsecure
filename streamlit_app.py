# streamlit_app.py
# Main application file for the RailSecure Learning Platform.
# This script initializes the Streamlit app, sets up page configurations,
# handles navigation between different training modules, and orchestrates
# the overall application flow.

import streamlit as st
from PIL import Image # Pillow library for image manipulation, used here for favicon
from utils.helpers import ( # Importing utility functions
    get_openai_client,
    set_app_background,
    init_session_state,
    get_nvd_api_key
)

# Importing display functions for each module from the 'modules' package
from modules import home_module
from modules import phishing_module
from modules import password_module
from modules import scenario_quiz_module
from modules import compliance_module
from modules import incident_response_module
from modules import cybersecurity_quiz_module
from modules import cve_explainer_module
from modules import reference_module
from modules import security_awareness_importance_module

# ---------------------------------------------------
# Configure the Streamlit page
# This must be the first Streamlit command in the app.
# ---------------------------------------------------
# Load the favicon image
# Note: Streamlit also accepts a file path string directly for page_icon.
# Using PIL Image object here as per user's preference/example.
try:
    icon_image = Image.open("assets/favicon.png") # Path to the favicon image
except FileNotFoundError:
    st.warning("Favicon 'assets/favicon.png' not found. Using default emoji icon.")
    icon_image = "🛡️" # Fallback emoji icon if the image file is not found
except Exception as e:
    st.error(f"Error loading favicon: {e}")
    icon_image = "🛡️" # Fallback emoji icon on other errors

st.set_page_config(
    page_title="RailSecure Learning Platform", # Title displayed in the browser tab
    page_icon=icon_image,                     # Icon displayed in the browser tab (favicon)
    layout="centered",                        # Page layout: "centered" or "wide"
    initial_sidebar_state="expanded"          # How the sidebar initially appears: "auto", "expanded", "collapsed"
)

# Apply custom background style and initialize session state variables
set_app_background() # Sets the custom background for the app
init_session_state() # Initializes or ensures all necessary session state keys exist

# Initialize OpenAI client (for modules requiring LLM interaction)
# and NVD API Key (for the CVE explainer module, optional)
openai_client = get_openai_client()
nvd_api_key = get_nvd_api_key()

# ---------------------------------------------------
# Main Application Logic
# ---------------------------------------------------
def main():
    """
    Main function to render the Streamlit application.
    Sets up the page header (logo and title), sidebar for navigation,
    and then calls the appropriate module's display function based on user selection.
    """
    
    # --- Display Logo and Title (Logo Above Title) ---
    try:
        # Display the application logo from the assets folder
        st.image("assets/logo.png", width=125) # Adjust width as needed
    except FileNotFoundError:
        # Display an error if the logo file is not found
        st.error("Logo image (assets/logo.png) not found. Please add it to the assets folder.")
    except Exception as e:
        # Display an error for any other issues loading the logo
        st.error(f"Error loading logo: {e}")
    
    # Display the main application title using Markdown for custom styling (margin control)
    st.markdown("<h1 style='margin-top: -0.7em; margin-bottom: 0.5em;'>RailSecure Learning Platform</h1>", unsafe_allow_html=True)

    # --- Sidebar Menu for Navigation ---
    # Define the list of available training modules
    menu = [
        "Home",
        "Phishing Training",
        "Password Generator & Tips", 
        "Incident Scenario Simulation", 
        "Compliance Hub", 
        "Incident Response Guides", 
        "Cybersecurity Knowledge Quiz", 
        "Latest CVE Insights", 
        "Regulatory & Best Practice References", 
        "Why Security Awareness Matters" 
    ]
    # Create a selectbox in the sidebar for module selection
    choice = st.sidebar.selectbox(
        "Select Training Module", 
        menu, 
        help="Navigate through different cybersecurity training modules."
    )

    # --- Display Selected Module ---
    # Conditional rendering based on the user's choice from the sidebar.
    # The OpenAI client and NVD API key are passed to modules that require them.

    # Check if OpenAI client is needed and not available for certain modules
    if not openai_client and choice not in [
        "Home", "Password Generator & Tips", "Latest CVE Insights", 
        "Why Security Awareness Matters", "Regulatory & Best Practice References" 
        # Modules listed here can function without openai_client
    ]:
        st.error("OpenAI client could not be initialized. AI-powered features in this module are unavailable. Please check your API key in secrets.")
        # App proceeds, but AI-dependent parts of the module won't work.
        # Modules are expected to handle a None openai_client gracefully if they have non-AI parts.

    # Main content area container with a border for visual separation
    with st.container(border=True): 
        if choice == "Home":
            home_module.display_home()
        elif choice == "Phishing Training":
            # Phishing module requires openai_client
            if openai_client:
                phishing_module.display_phishing_training(openai_client)
            else:
                st.warning("Phishing Training module's AI features require an active OpenAI client.")
                # Consider if this module has parts that can run without AI,
                # if so, call display_phishing_training(None) and handle None in the module.
        elif choice == "Password Generator & Tips":
            password_module.display_password_generator()
        elif choice == "Incident Scenario Simulation":
            # Scenario simulation requires openai_client
            if openai_client:
                scenario_quiz_module.display_scenario_quiz(openai_client)
            else:
                st.warning("Incident Scenario Simulation module's AI features require an active OpenAI client.")
        elif choice == "Compliance Hub":
            # Compliance hub has both static content and AI Q&A
            compliance_module.display_compliance_hub(openai_client) # Module handles if client is None
        elif choice == "Incident Response Guides":
            # Incident response guides have static content and AI custom guide generation
            incident_response_module.display_incident_response_guide(openai_client) # Module handles
        elif choice == "Cybersecurity Knowledge Quiz":
            # Cybersecurity quiz requires openai_client for question generation
            if openai_client:
                cybersecurity_quiz_module.display_cybersecurity_quiz(openai_client)
            else:
                st.warning("Cybersecurity Knowledge Quiz module's AI features require an active OpenAI client.")
        elif choice == "Latest CVE Insights":
            cve_explainer_module.display_cve_explainer(nvd_api_key) # Uses NVD API key
        elif choice == "Regulatory & Best Practice References":
            # Reference materials have static links and AI Q&A
            reference_module.display_reference_materials(openai_client) # Module handles
        elif choice == "Why Security Awareness Matters":
            security_awareness_importance_module.display_importance_of_security_awareness()
        # To add new modules, include an elif block here and import the module at the top.

# ---------------------------------------------------
# Run the main application
# Ensures that main() is called only when the script is executed directly.
# ---------------------------------------------------
if __name__ == "__main__":
    main()
