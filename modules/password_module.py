# modules/password_module.py
# This module provides functionality for password generation and strength checking.
# It includes a password generator based on user-defined criteria (length, character types)
# and a strength checker utilizing the 'zxcvbn' library for robust analysis.
# It also displays tips for creating strong passwords.

import streamlit as st
import random           # For random selection of characters in password generation
import string           # For predefined character sets (lowercase, uppercase, digits)
from zxcvbn import zxcvbn # Library for advanced password strength estimation

# --- Password Generation Logic ---

def _generate_password(length=12, use_uppercase=True, use_digits=True, use_special_chars=True):
    """
    Generates a random password based on specified criteria.

    Args:
        length (int): The desired length of the password.
        use_uppercase (bool): Whether to include uppercase letters.
        use_digits (bool): Whether to include numeric digits.
        use_special_chars (bool): Whether to include special characters.

    Returns:
        str: The generated random password.
    """
    # Start with lowercase letters as a base character pool
    char_pool = string.ascii_lowercase
    
    # Conditionally add other character types to the pool
    if use_uppercase:
        char_pool += string.ascii_uppercase
    if use_digits:
        char_pool += string.digits
    if use_special_chars:
        # Define a set of common, easily typable special characters
        char_pool += "!@#$%^&*()-_=+[]{};:,.<>/?"

    # Fallback if no character types were selected (though lowercase is always included by default)
    if not char_pool: 
        char_pool = string.ascii_lowercase # Should not be reached with current logic

    # Generate a list of random characters from the pool
    password_chars = [random.choice(char_pool) for _ in range(length)]
    
    # Shuffle the characters to ensure randomness of their positions in the final password
    random.shuffle(password_chars)
    # Join the characters to form the final password string
    return "".join(password_chars)

# --- Password Strength Checking Logic ---

def check_password_strength_with_zxcvbn(password_to_check, user_specific_inputs=None):
    """
    Checks password strength using the zxcvbn library, providing a qualitative score
    and detailed feedback including warnings, suggestions, and estimated crack times.

    Args:
        password_to_check (str): The password string to evaluate.
        user_specific_inputs (list, optional): A list of strings (e.g., username, real name)
                                               that should be considered weak if part of the password.
                                               Defaults to None (empty list).

    Returns:
        tuple: (strength_level_str, feedback_messages_list)
               - strength_level_str: A human-readable strength level (e.g., "🔴 Very Weak").
               - feedback_messages_list: A list of strings containing detailed feedback.
    """
    if not password_to_check: # Handle empty password input
        return "⚪ N/A", ["Please enter a password to check its strength."]
    
    if user_specific_inputs is None: # Ensure user_inputs is always a list for zxcvbn
        user_specific_inputs = []
        
    # Perform password strength analysis using zxcvbn
    results = zxcvbn(password_to_check, user_inputs=user_specific_inputs)
    score = results['score']  # zxcvbn score: 0 (worst) to 4 (best)
    
    feedback_messages = [] # List to hold feedback items

    # Map zxcvbn score to a human-readable strength level and color emoji
    strength_levels = {
        0: "🔴 Very Weak", 1: "🟠 Weak", 2: "🟡 Moderate",
        3: "🟢 Strong", 4: "🔵 Very Strong"
    }
    level = strength_levels.get(score, "⚪ Unknown") # Default if score is out of expected range
    
    # Provide a nuanced interpretation if the score is high but crack time is very low
    # (indicating common patterns or dictionary words despite complexity score)
    crack_time_display = results['crack_times_display'].get('offline_fast_hashing_1e10_per_second', 'N/A')
    if score >= 3 and (crack_time_display == 'less than a second' or 
                       'seconds' in crack_time_display or 
                       'minutes' in crack_time_display): # Check for short crack times
        feedback_messages.append(
            f"⚠️ **Heads up!** While rated as '{level.split(' ')[1]}', this password contains patterns or words that make it easier to guess than its score might suggest."
        )
        level = f"{level} (but potentially guessable)" # Modify the displayed level

    # Add the raw score for context
    feedback_messages.append(f"📊 **Overall zxcvbn Score:** {score}/4")

    # Add warnings and suggestions from zxcvbn's analysis
    if results['feedback']['warning']:
        feedback_messages.append(f"🚫 **Warning from zxcvbn:** {results['feedback']['warning']}")
    for suggestion in results['feedback']['suggestions']:
        feedback_messages.append(f"💡 **Suggestion from zxcvbn:** {suggestion}")

    # Add estimated crack time
    feedback_messages.append(f"⏳ **Est. time to crack (fast offline hash scenario):** {crack_time_display}")
    
    return level, feedback_messages

# --- Static Content Display Functions ---

def _display_password_tips():
    """
    Displays a list of best practices for creating and managing strong passwords
    within an expander.
    """
    st.subheader("🛡️ Tips for Strong Password Creation & Best Practices")
    with st.expander("Click here to view essential password tips and best practices.", expanded=False):
        # Detailed markdown content with password tips
        st.markdown(
            """
            Creating strong, unique passwords is a critical first step in protecting your accounts and Iarnród Éireann's data. Here are some key tips:

            * **Length is Strength:** Aim for at least **12-16 characters**. Longer passwords are significantly harder to crack.
            * **Mix It Up:** Include a combination of:
                * Uppercase letters (A-Z)
                * Lowercase letters (a-z)
                * Numbers (0-9)
                * Special characters (e.g., `!@#$%^&*()`)
            * **Avoid the Obvious:** Don't use easily guessable information such as personal names, birthdays, common words, or company names (e.g., "IrishRailSecure").
            * **Uniqueness is Key:** Use a **different password for every account**. If one account is compromised, others remain safe.
            * **Consider Passphrases:** Create a long, memorable passphrase by combining several random words (e.g., "CorrectHorseBatteryStaple"). You can enhance these with numbers and symbols.
            * **Use a Password Manager:** These tools securely store and generate complex passwords for you. This is highly recommended for managing many unique passwords.
            * **Beware of Phishing:** Never reveal your password in response to an email or unsolicited request. Iarnród Éireann IT will never ask for your password via email.
            * **Enable Multi-Factor Authentication (MFA):** Wherever possible, enable MFA (also known as 2FA). This adds an extra layer of security beyond just your password.
            * **Regular Updates (Strategically):** Modern guidance emphasizes changing passwords primarily if you suspect a compromise, rather than on a fixed frequent schedule. Focus on strength and uniqueness.

            By following these guidelines, you significantly enhance your digital security.
            """
        )

# --- Main Display Function for the Module ---

def display_password_generator():
    """
    Displays the main UI for the Password Generator & Security Tips module.
    Includes a form for password generation options, displays the generated password
    with its strength analysis, and provides a section for users to check the
    strength of their own passwords.
    """
    st.subheader("🔑 Password Generator & Security Tips")
    st.write(
        "Use this tool to generate strong, random passwords and check password strength. "
        "Remember to store generated passwords securely, ideally using a password manager."
    )
    st.markdown("---") # Visual separator
    
    # --- Password Generation Section ---
    # Use a form for batching input for password generation
    with st.form(key="password_generator_form"):
        st.markdown("#### Configure Password Generation Parameters:")
        # Slider for password length
        length = st.slider(
            "Password Length:", min_value=8, max_value=32, value=16, step=1,
            help="Longer passwords are more secure. Aim for at least 12-16 characters."
        )
        # Checkboxes for character type inclusion
        use_uppercase = st.checkbox("Include Uppercase Letters (A-Z)", value=True, key="pw_upper_checkbox")
        use_digits = st.checkbox("Include Numbers (0-9)", value=True, key="pw_digits_checkbox")
        use_special = st.checkbox("Include Special Characters (e.g., !@#$%&*)", value=True, key="pw_special_checkbox")
        
        # Submit button for the form
        submitted_generate = st.form_submit_button(label="✨ Generate Secure Password")

    # Process password generation if form submitted
    if submitted_generate:
        # Warn if complexity options are minimal (e.g., only lowercase selected implicitly)
        if not (use_uppercase or use_digits or use_special) and length > 0 : 
             st.warning("For stronger passwords, ensure you include a mix of character types along with sufficient length.")
        
        generated_pwd = _generate_password(length, use_uppercase, use_digits, use_special)
        st.session_state["generated_password"] = generated_pwd # Store in session state
        
        # Check strength of the newly generated password
        level, feedback = check_password_strength_with_zxcvbn(generated_pwd)
        st.session_state["generated_password_strength"] = level
        st.session_state["generated_password_feedback"] = feedback
        
    # Display generated password and its strength if available in session state
    if st.session_state.get("generated_password"):
        st.markdown("---")
        st.markdown("#### Your Generated Password:")
        st.code(st.session_state["generated_password"], language="text") # Display password in a code block
        
        # Display strength analysis for the generated password
        if st.session_state.get("generated_password_strength"):
            st.write(f"**Strength:** {st.session_state['generated_password_strength']}")
            with st.expander("Show strength details for generated password", expanded=True): # Open by default
                for item in st.session_state.get("generated_password_feedback", []):
                    st.markdown(f"* {item}") # Use markdown for itemized feedback
        
        st.info("✅ Password generated! Copy it and store it securely.")
        # Button to clear the generated password and its analysis from display
        if st.button("Clear Generated Password", key="clear_generated_pwd_button"):
            st.session_state["generated_password"] = None
            st.session_state["generated_password_strength"] = None
            st.session_state["generated_password_feedback"] = None
            st.rerun() # Rerun to update the UI

    st.markdown("---") # Visual separator

    # --- Manual Password Strength Checker Section ---
    st.markdown("#### Check Your Own Password Strength")
    # Input field for user to type their password (masked)
    user_password_to_check = st.text_input(
        "Enter a password to check:", 
        type="password", # Hides the typed characters
        key="user_password_check_input" 
    )

    # If user has entered a password, check and display its strength
    if user_password_to_check: 
        # For this implementation, user_specific_inputs is not collected from UI, so it's passed as None.
        level, feedback = check_password_strength_with_zxcvbn(user_password_to_check) 
        
        st.write(f"**Strength Analysis:** {level}")
        # Display detailed feedback in an expander, open by default
        with st.expander("Show strength details for your password", expanded=True): 
            for item in feedback:
                st.markdown(f"* {item}")
    else:
        # Prompt user if the input field is empty
        st.caption("Type a password above to see its strength analysis.")
    
    st.markdown("---") # Visual separator
    _display_password_tips() # Display general password tips
