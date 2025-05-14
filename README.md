<div align="center">
  <img src="./assets/logo.png" alt="RailSecure Platform Logo" width="170px">
  <h1>RailSecure Learning Platform</h1>
  <p><strong>An Interactive Cyber-Security Awareness & Training Tool</strong></p>
  <p><em>Developed as part of a Cyber-Security Graduate interview with Iarnród Éireann (Irish Rail)</em></p>
  <hr/>
</div>

> **⚠️ Disclaimer**  
> RailSecure was created as a **proof-of-concept portfolio project** for an interview task.  
> It has **not** passed penetration testing or production hardening; use at your own risk.  
> The code is released under the MIT Licence so you may adapt it freely, but please audit thoroughly before any live deployment.

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Project Genesis & Objectives](#2-project-genesis--objectives)
3. [Key Features](#3-key-features)
4. [Technology Stack](#4-technology-stack)
5. [Architecture & Code Layout](#5-architecture--code-layout)
   * [5.1 Directory Tree](#51-directory-tree)
   * [5.2 Core File Descriptions](#52-core-file-descriptions)
6. [Getting Started & Deployment](#6-getting-started--deployment)
   * [6.1 Online Deployment (Streamlit Cloud)](#61-online-deployment-streamlit-cloud)
   * [6.2 Local / Offline Run](#62-local--offline-run)
7. [Limitations & Future Work](#7-limitations--future-work)
8. [Licence](#8-licence)
9. [Developer’s Note](#9-developers-note)
10. [Live Demo](#10-live-demo)

---

## 1. Introduction

**RailSecure** is an interactive web application designed to showcase how a modern security-awareness programme could be delivered inside a rail operator such as Iarnród Éireann. Using **Streamlit** for rapid UI development and **OpenAI GPT-4o** for dynamic content, the platform demonstrates practical learning modules covering phishing, password hygiene, incident response, regulatory compliance and more.

---

## 2. Project Genesis & Objectives

The interview brief asked candidates to present on:

> *“Cyber-security regulations that Irish Rail must abide by, tools that aid compliance, and how to set up a security-awareness programme.”*

Rather than deliver a static slide-deck, I built RailSecure to:

* **💡 Demonstrate innovation** – show an engaging, hands-on learning environment.
* **🛠️ Provide practical tooling** – quizzes, phishing drills, CVE feeds, incident simulations.
* **📜 Embed compliance context** – NIS2, GDPR, CER Directive, ISO 27001, IEC 62443.
* **🤖 Leverage AI** – generate fresh scenarios, evaluate answers, power live Q&A.
* **🛡️ Promote security culture** – illustrate how every employee becomes a defence layer.

---

## 3. Key Features

| Module | Purpose |
|--------|---------|
| **Home** | Welcome, feature overview, Dublin-localised time & version. |
| **Phishing Awareness** | AI-generated phishing emails · User explains red flags · AI feedback · “Paste-your-own” email analyser. |
| **Password Tools** | Secure password generator · `zxcvbn` strength checker · best-practice tips. |
| **Incident Scenario Simulation** | GPT-crafted OT/IT incident narrative · user submits response strategy · AI critique. |
| **Incident Response Guides** | Generic 6-phase framework · AI-generated scenario-specific guides inc. NIS2/GDPR timelines. |
| **Compliance Hub** | Expanders on SIEM/SOAR/GRC, IAM, OT security · blueprint for awareness programme · live compliance Q&A. |
| **Cyber-Security Quiz** | GPT-generated MCQs · instant scoring · explanations. |
| **CVE Explainer** | Pulls latest 30-day CVEs from NVD · shows CVSS v3.1 severity. |
| **Reference Library** | Curated links to directives & standards · AI Q&A. |
| **Why Awareness Matters** | Case-study gallery of real-world transport cyber incidents. |

Session state ensures a seamless multi-page experience.

---

## 4. Technology Stack

| Layer | Tech | Notes |
|-------|------|-------|
| **Front-end / UI** | [Streamlit 1.x](https://streamlit.io) | Custom CSS (dark theme, hero background). |
| **Backend / Language** | Python 3.9+ | Typed where helpful; no external DB required. |
| **AI / LLM** | [OpenAI Python SDK](https://github.com/openai/openai-python) | GPT-4o with tuned temperature per task. |
| **Password Analysis** | [`zxcvbn`](https://github.com/dropbox/zxcvbn) | Crack-time estimation & feedback. |
| **External Data** | NVD CVE API v2 (via `requests`) | Live vulnerability feed. |
| **Assets** | Local images (logo, favicon, background) | No external CDN. |
| **Deployment** | Streamlit Community Cloud | Free tier; secrets stored server-side. |

---

## 5. Architecture & Code Layout

### 5.1 Directory Tree
```

.
├── streamlit\_app.py        # Main router & sidebar
├── requirements.txt
│
├── assets/
│   ├── background.jpg
│   ├── favicon.png
│   └── logo.png
│
├── utils/
│   ├── helpers.py          # OpenAI client, CSS injection, session init, LLM helpers
│   └── **init**.py
│
└── modules/                # One file per feature
├── compliance\_module.py
├── cve\_explainer\_module.py
├── cybersecurity\_quiz\_module.py
├── home\_module.py
├── incident\_response\_module.py
├── password\_module.py
├── phishing\_module.py
├── reference\_module.py
├── scenario\_quiz\_module.py
├── security\_awareness\_importance\_module.py
└── **init**.py

````

### 5.2 Core File Descriptions

| File | Role |
|------|------|
| **`streamlit_app.py`** | Sets page config, calls `utils.helpers.init_session_state()`, provides sidebar navigation and lazy-loads each module’s `display_*` function. |
| **`requirements.txt`** | Lightweight dependency list. |
| **`utils/helpers.py`** | • OpenAI & NVD key retrieval<br>• CSS background injector<br>• Session-state defaults<br>• `create_llm_messages()` helper. |
| **`modules/*.py`** | Self-contained pages; each exports a single `display_*()` that builds all Streamlit widgets and (if needed) calls OpenAI. |
| **`assets/`** | Static imagery (brand consistency & UX). |

---

## 6. Getting Started & Deployment

### 6.1 Online Deployment (Streamlit Cloud)

1. **Fork / clone** the repo to GitHub → <https://github.com/rsvptr/railsecure>.  
2. Sign in at <https://streamlit.io/cloud>, click **“New app”**.  
3. Select repository & branch, set **Main file** = `streamlit_app.py`.  
4. In *Advanced Settings* → **Secrets**, add:
   ```toml
   OPENAI_API_KEY = "sk-..."
   # Optional – boosts NVD rate-limit
   NVD_API_KEY    = "your-nvd-key"


5. Deploy.

### 6.2 Local / Offline Run

```bash
# 1 Clone
git clone https://github.com/rsvptr/railsecure.git
cd railsecure

# 2 (Recommended) Create virtual-env
python -m venv .venv
# Linux / Others
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

# 3 Install deps
pip install -r requirements.txt

# 4 Secrets
mkdir -p .streamlit
cat > .streamlit/secrets.toml <<'EOF'
OPENAI_API_KEY = "sk-..."
# NVD_API_KEY  = "..."
EOF

# 5 Run
streamlit run streamlit_app.py
```

Navigate to [http://localhost:8501](http://localhost:8501).

---

## 7. Limitations & Future Work

* **No Auth / RBAC** – anyone with the URL can access; production would need SSO or IAM.
* **Security Hardening** – headers, CSP, rate-limit, input sanitisation not yet audited.
* **Persistence** – all user state lives in browser session; could consider SQLite or Postgres.
* **Automated Testing** – manual QA only; adding `pytest` + Streamlit’s test client would raise quality.
* **LMS Integration** – SCORM/xAPI export or REST hooks could allow HR tracking.
* **Internationalisation** – English-only; potential LLM translation.

---

## 8. Licence

Released under the **MIT License** – see `LICENSE` or [https://opensource.org/licenses/MIT](https://opensource.org/licenses/MIT).

In short: do anything you like, but give credit and don’t sue the author if it breaks.

---

## 9. Developer’s Note

Building RailSecure pushed me to blend **pedagogy**, **regulatory knowledge**, and **code craftsmanship** into a single deliverable under interview time-pressure.
The project reaffirmed that **hands-on, scenario-based learning** resonates far more than theory alone. I hope it also demonstrates my ability to turn vague requirements into a polished, user-friendly product.

Feel free to explore, fork, and improve – and let me know if it helps your own security-awareness journey!

---

## 10. Live Demo

👉 **Explore the running app here:** [https://railsecure.streamlit.app](https://railsecure.streamlit.app)  🎉
