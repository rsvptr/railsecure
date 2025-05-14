# modules/__init__.py
# This file signifies that the 'modules' directory should be treated as a Python package.
# This allows for organized importing of individual modules (e.g., `from modules import home_module`).

"""
The 'modules' package for the RailSecure Learning Platform.

This directory contains individual Python modules, each encapsulating the UI
and logic for a distinct feature or section of the Streamlit application.
This modular structure enhances code organization, maintainability, and scalability.

Examples of modules found within this package:
    - `home_module.py`: Displays the main landing page.
    - `phishing_module.py`: Handles phishing simulation and email analysis.
    - `password_module.py`: Provides password generation and strength checking.
    - `cve_explainer_module.py`: Fetches and displays CVE information.
    # ... and so on for all other application features.

Each module typically exports a primary display function (e.g., `display_home()`, 
`display_phishing_training()`) which is invoked by the main `streamlit_app.py` 
script to render the corresponding part of the application.
"""

# This __init__.py file can remain empty if no package-level variables, 
# functions, or sub-package imports need to be defined here. Its presence is
# sufficient to make 'modules' an importable package.
