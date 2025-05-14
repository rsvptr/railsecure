# utils/__init__.py
# This file marks the 'utils' directory as a Python package.
# It allows modules within 'utils' (like helpers.py) to be imported elsewhere in the application,
# for example, using `from utils.helpers import ...`.

"""
The 'utils' package for the RailSecure Learning Platform.

This directory houses utility functions and helper classes that are shared
across various modules of the application. The primary goal is to promote 
code reusability and centralize common functionalities.

Key contents:
    - `helpers.py`: Contains functions for:
        - OpenAI API client initialization.
        - NVD API key retrieval.
        - Custom UI styling (e.g., app background).
        - Session state management.
        - Structuring messages for LLM API calls.

Centralizing these utilities helps maintain consistency and simplifies updates
to shared application logic.
"""

# This file can remain empty if no package-level initializations 
# or specific exports from the 'utils' package itself are needed.
# For instance, to directly expose a function from helpers.py at the 'utils' package level,
# you could add: `from .helpers import get_openai_client`
# This would allow imports like `from utils import get_openai_client`.
# However, the current project structure uses explicit submodule imports (e.g., `from utils.helpers import ...`),
# which is often preferred for clarity in larger projects.
