<div align="center">
  <img src="./assets/logo.png" alt="RailSecure Platform Logo" width="170px">
  <h1>RailSecure</h1>
  <p><strong>An Interactive Cybersecurity Awareness & Training Tool</strong></p>
  <p><em>Developed as part of an interview task with Iarnród Éireann (Irish Rail)</em></p>
  <hr/>
</div>

## Table of Contents

- [1. Introduction](#1-introduction)
- [2. Project Genesis and Objectives](#2-project-genesis-and-objectives)
- [3. Key Features and Functionalities](#3-key-features-and-functionalities-)
- [4. Technology Stack](#4-technology-stack-️)
- [5. Implementation Insights: Code Structure & Design](#5-implementation-insights-code-structure--design-️)
  - [5.1. Project Directory Layout](#51-project-directory-layout)
  - [5.2. Core File Descriptions](#52-core-file-descriptions)
- [6. Deployment and Setup Instructions](#6-deployment-and-setup-instructions-️)
  - [6.1. Online Deployment (Streamlit Community Cloud)](#61-online-deployment-streamlit-community-cloud)
  - [6.2. Local Deployment / Development Setup](#62-local-deployment--development-setup)
- [7. License](#7-license-)
- [8. Developer's Note](#8-developers-note-️)

---

## 1. Introduction

Welcome to the **RailSecure Learning Platform**! This interactive web application was conceived and meticulously developed as a substantial component of a presentation for a Cybersecurity Graduate role interview with Iarnród Éireann (Irish Rail). Its primary objective is to demonstrate a practical, engaging, and multifaceted approach to constructing and implementing a security awareness programme, specifically tailored for an organization operating critical national infrastructure.

The platform serves as a dynamic showcase of how modern web technologies and AI can be leveraged to create impactful educational experiences in cybersecurity.

> **⚠️ Important Disclaimer:** This platform is a proof-of-concept and a demonstration tool, primarily developed for an interview setting. While functionally robust for its intended purpose of exploration and pedagogical demonstration, it is **not intended for production-level deployment or operational use within a live corporate environment.** Any such use would require significant further development, rigorous security hardening, comprehensive code audits, and thorough quality assurance processes.

---

## 2. Project Genesis and Objectives

The impetus for RailSecure stemmed from a specific interview task: *"Cybersecurity Regulations that Irish Rail must abide by and tools that can be used aid in compliance - and how would one go about setting up a security awareness programme."*

Rather than limiting the response to a purely theoretical discussion, this platform was created to provide a tangible, interactive demonstration of how various components of a modern security awareness programme could be effectively realized. The core objectives underpinning its development were to:

* 💡 Illustrate innovative and engaging methods for enhancing cybersecurity knowledge and vigilance among Iarnród Éireann staff.

* 🛠️ Provide practical, hands-on modules covering critical areas such as phishing detection, password security best practices, and incident response preparedness.

* 📜 Integrate information regarding pertinent cybersecurity regulations and standards (e.g., NIS2 Directive, GDPR, CER Directive, ISO 27001, IEC 62443) within a relevant and accessible context.

* 🤖 Showcase the potential of AI-driven tools (leveraging Large Language Models) for generating dynamic training content, providing interactive Q&A sessions, and evaluating user responses in real-time.

* 🛡️ Ultimately, to foster a proactive, informed, and resilient security culture across the organization by making learning engaging, relevant, and accessible.

---

## 3. Key Features and Functionalities 🚀

The RailSecure Learning Platform is a modular application, with each module designed to address a specific facet of cybersecurity awareness and training:

* 🏡 **Home Section (`home_module.py`):**
    The main landing page, offering a welcome message, an overview of platform features, and dynamic info like current date/time (Dublin localized) and application version.

* 🎣 **Phishing Awareness Training (`phishing_module.py`):**
    Features AI-driven phishing email simulation, user analysis with AI feedback, and an "Analyze My Email" tool for assessing user-pasted suspicious emails.

* 🔑 **Password Security Tools (`password_module.py`):**
    Includes a secure password generator, an advanced strength analyzer using `zxcvbn`, and displays best practices for password management.

* 🛡️ **Incident Scenario Practice (`scenario_quiz_module.py`):**
    Offers AI-generated cybersecurity incident scenarios tailored to a rail environment, allowing users to propose response strategies that are then evaluated by an AI trainer.

* 🏛️ **Compliance Information Hub (`compliance_module.py`):**
    Presents information on key compliance tools (SIEM, SOAR, etc.), outlines security awareness program essentials, and features an interactive AI Q&A on NIS2, GDPR, and related topics.

* 📖 **Incident Response Guides (`incident_response_module.py`):**
    Details a general incident response framework (including regulatory reporting timelines) and allows generation of custom, AI-powered guides for specific incident categories.

* 🧠 **Cybersecurity Quiz (`cybersecurity_quiz_module.py`):**
    Utilizes AI to dynamically generate multiple-choice quizzes on cybersecurity topics relevant to Iarnród Éireann, providing interactive assessment and instant feedback.

* ⚠️ **CVE Vulnerability Updates (`cve_explainer_module.py`):**
    Fetches and displays real-time information on recent Common Vulnerabilities and Exposures (CVEs) from the National Vulnerability Database (NVD), including CVSS scores.

* 📚 **Regulatory & Standards Information (`reference_module.py`):**
    Provides curated links to official documentation for key regulations (NIS2, GDPR, etc.) and industry standards (ISO 27001, IEC 62443), supplemented by an AI Q&A feature.

* 💡 **Importance of Security Awareness (`security_awareness_importance_module.py`):**
    Explains the critical role of security awareness, featuring case studies of notable cyber incidents in the global transport sector to highlight potential impacts and lessons.

---

## 4. Technology Stack 🛠️

The RailSecure Learning Platform is built using a modern, Python-centric technology stack:

* **Core Framework:** [Streamlit](https://streamlit.io/)
* **Programming Language:** Python (3.9+ recommended)
* **Artificial Intelligence / LLMs:** [OpenAI API](https://openai.com/api/) (specifically `gpt-4o`)
* **Password Strength Assessment:** [zxcvbn-python](https://pypi.org/project/zxcvbn/)
* **External Data Integration:** NVD API, `requests` library
* **Image Handling:** `Pillow` (PIL Fork)
* **Date & Time Localization:** Python `datetime` and `zoneinfo`
* **Styling:** Custom CSS injected via Streamlit
* **Development Environment:** `venv`, Git

---

## 5. Implementation Insights: Code Structure & Design 🏛️

The project adheres to a modular design philosophy for clarity and maintainability.

### 5.1. Project Directory Layout

```text
railsecure/
│
├─── assets/              # Static assets (images, logos, icons)
│    ├── background.jpg
│    ├── favicon.png
│    └── logo.png
│
├─── modules/             # Individual feature/learning modules
│    ├── compliance_module.py
│    ├── cve_explainer_module.py
│    ├── cybersecurity_quiz_module.py
│    ├── home_module.py
│    ├── incident_response_module.py
│    ├── password_module.py
│    ├── phishing_module.py
│    ├── reference_module.py
│    ├── scenario_quiz_module.py
│    ├── security_awareness_importance_module.py
│    └── __init__.py      # Initializes 'modules' as a Python package
│
├─── utils/               # Shared utility functions
│    ├── helpers.py
│    └── __init__.py      # Initializes 'utils' as a Python package
│
├─── .streamlit/          # Streamlit-specific configuration
│    └── secrets.toml     # (User-created) For API keys
│
├─── .gitignore           # Specifies files for Git to ignore
├─── requirements.txt     # Project dependencies
└─── streamlit_app.py     # Main application entry point
````

### 5.2. Core File Descriptions

  * **`streamlit_app.py`**: Main application script; handles page config, navigation, and module loading.
  * **`requirements.txt`**: Lists all Python package dependencies for the project.
  * **`assets/`**: Contains static files like images (`background.jpg`, `favicon.png`, `logo.png`).
  * **`utils/__init__.py`**: Marks `utils` directory as a Python package.
  * **`utils/helpers.py`**: Contains shared utility functions (API client init, UI styling, session state, LLM prompt formatting).
  * **`modules/__init__.py`**: Marks `modules` directory as a Python package.
  * **`modules/*.py`**: Each file implements a specific feature module as detailed in Section 3 (e.g., `home_module.py` handles the Home Section).

-----

## 6\. Deployment and Setup Instructions ⚙️

This application can be deployed online via Streamlit Community Cloud or run locally.

### 6.1. Online Deployment (Streamlit Community Cloud)

1.  **Prerequisites:** GitHub account, project repository on GitHub, Streamlit Community Cloud account.
2.  **Repository Prep:** Ensure `streamlit_app.py` is the main file and `requirements.txt` is accurate. **Do not commit `secrets.toml` or API keys.**
3.  **Deployment:**
      * Log in to [Streamlit Community Cloud](https://streamlit.io/cloud).
      * Click "New app," select your repository, branch, and main file path.
      * **Configure Secrets:** In advanced settings, add `OPENAI_API_KEY` and optional `NVD_API_KEY` with their values.
      * Click "Deploy\!".
4.  **Access:** Use the provided URL (e.g., `https://your-app-name.streamlit.app`).

### 6.2. Local Deployment / Development Setup

1.  **Clone Repository:**

    ```bash
    git clone [https://github.com/rsvptr/railsecure.git](https://github.com/rsvptr/railsecure.git)
    cd railsecure
    ```

2.  **Create & Activate Virtual Environment:**

    ```bash
    python -m venv venv
    # On macOS/Linux:
    source venv/bin/activate
    # On Windows (Cmd/PowerShell):
    venv\Scripts\activate or .\venv\Scripts\Activate.ps1
    ```

3.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure API Keys Locally:**

      * Create directory: `mkdir .streamlit` (in project root).
      * Create file: `.streamlit/secrets.toml`.
      * Add keys to `secrets.toml`:
        ```toml
        OPENAI_API_KEY = "sk-YourActualOpenAIAPIKeyGoesHere"
        # NVD_API_KEY = "YourActualNVDAPIKeyGoesHere_IfYouHaveOne" # Optional
        ```
      * Ensure `.streamlit/secrets.toml` is in your `.gitignore`.

5.  **Run Application:**

    ```bash
    streamlit run streamlit_app.py
    ```

    Access typically at `http://localhost:8501`.

-----

**🔴 Live Deployment Note:** The publicly accessible live deployment of this application can be found at: [**https://railsecure.streamlit.app**](https://railsecure.streamlit.app)

-----

## 7\. License 📜

This project is made available under the terms of the **MIT License**.

This permissive license allows you to freely share and adapt the material for any purpose, provided you give appropriate credit to the original author, include the original copyright notice, and indicate if changes were made. The software is provided "as is", without warranty of any kind.

For full details, please refer to a standard MIT License text or the `LICENSE` file if one is included in the repository.

-----

## 8\. Developer's Note 🧑‍💻

The development of the RailSecure Learning Platform was an engaging and intellectually stimulating endeavor, undertaken with the specific aim of fulfilling an interview requirement for a Cybersecurity Graduate role. It provided an invaluable opportunity to explore the practical application of web development (via Streamlit), API integration (OpenAI, NVD), and AI-driven content generation in cybersecurity education.

While this platform serves as a demonstration, the process underscored the complexities in building effective and secure training tools. Numerous avenues exist for expansion, such as user tracking, gamification, broader scenario libraries, and LMS integration, should this evolve beyond a proof-of-concept.

Thank you for taking the time to explore the RailSecure Learning Platform\!

Happy (and secure) learning\!

-----
