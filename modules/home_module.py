# modules/home_module.py
# This module defines the content and layout for the Home page of the 
# RailSecure Learning Platform. It serves as the main landing page for users.

import streamlit as st
from datetime import datetime # For displaying current date and time
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError # For timezone-aware datetime objects (Python 3.9+)

def display_home():
    """
    Displays the Home page content, including a welcome message,
    an overview of the platform's features, and current date/time/version information.
    """
    st.subheader("Welcome!") # Main greeting for the home page

    # Introductory paragraph about the platform's purpose
    st.markdown(
        """
        This interactive platform is your dedicated resource for enhancing cybersecurity awareness and skills 
        across Iarnród Éireann. In an era where digital threats are ever-present, your knowledge and vigilance 
        are crucial to protecting our passengers, our operations, and our critical national infrastructure.
        """
    )
    
    # Overview of features presented as a list using Markdown with hard line breaks
    # Each line ends with two spaces to create a line break without list bullets.
    # `&nbsp;` is used for a non-breaking space after emojis for better alignment.
    # `unsafe_allow_html=True` is required for `&nbsp;`.
    what_you_can_do_markdown = """
**What you can do here:**

🎣 &nbsp;**Phishing Training:** Learn to spot and report deceptive emails.  
🔑 &nbsp;**Password Security:** Generate strong passwords and understand best practices.  
🛡️ &nbsp;**Incident Simulation:** Test your response strategies in realistic scenarios.  
🏛️ &nbsp;**Compliance Hub:** Explore tools, programs, and ask AI about NIS2, GDPR, and more.  
📖 &nbsp;**Response Guides:** Access general and custom guides for handling cyber incidents.  
🧠 &nbsp;**Knowledge Quizzes:** Challenge your understanding of key security topics.  
⚠️ &nbsp;**CVE Insights:** Stay updated on the latest software vulnerabilities.  
📚 &nbsp;**Reference Materials:** Find links to important regulations and standards.  
🛡️ &nbsp;**Why Awareness Matters:** Understand the impact of cyber threats on the transport sector.
"""
    st.markdown(what_you_can_do_markdown, unsafe_allow_html=True) 
    
    # Informational message guiding the user
    st.info(
        "**Get Started:** Select a module from the sidebar on the left to begin your learning journey. "
        "Let's work together to build a more cyber-resilient Iarnród Éireann!"
    )

    # --- Display Current Time and Version ---
    try:
        # Attempt to get the current time localized to Europe/Dublin timezone
        dublin_tz = ZoneInfo("Europe/Dublin")
        now_in_dublin = datetime.now(dublin_tz)
        # Format the datetime object into a readable string
        time_display = now_in_dublin.strftime('%A, %B %d, %Y, %I:%M %p %Z')
    except ZoneInfoNotFoundError:
        # Fallback if the timezone info isn't found (e.g., older Python or minimal OS)
        time_display = f"{datetime.now().strftime('%A, %B %d, %Y, %I:%M %p')} (Server Time - Dublin timezone info not found)"
    except Exception as e:
        # General fallback for other errors during time localization
        time_display = f"{datetime.now().strftime('%A, %B %d, %Y, %I:%M %p')} (Server Time - Error localizing time: {e})"

    # Display the current date and time using st.caption for small, muted text
    st.caption(f"Current Date & Time: {time_display}")
    
    # Define application version and last updated date
    app_version = "v0.2.0" 
    last_updated = "14-May-2025" 
    # Display version information using st.caption
    st.caption(f"Platform Version: {app_version} (Last Updated: {last_updated})")
