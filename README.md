<div align="center">
  <img src="./assets/logo.png" alt="RailSecure Platform Logo" width="170px">
  <h1>RailSecure Learning Platform</h1>
  <p><strong>An Interactive Cyber-Security Awareness & Training Tool</strong></p>
  <p><em>Developed for a Cyber-Security Graduate interview with Iarnród Éireann (Irish Rail)</em></p>
  <hr/>
</div>

> **⚠️  Disclaimer**  
> RailSecure is a **proof-of-concept portfolio project**, created to accompany an interview presentation.  
> It has **not** undergone production-grade penetration testing or code review; deploy at your own risk.  
> Code is released under the **MIT Licence** – feel free to fork, but audit first.

---

## Table of Contents

1. [Introduction](#1-introduction)  
2. [Project Genesis & Objectives](#2-project-genesis--objectives)  
3. [Key Features](#3-key-features)  
4. [Technology Stack](#4-technology-stack)  
5. [Architecture & Code Layout](#5-architecture--code-layout)  
6. [Getting Started & Deployment](#6-getting-started--deployment)  
7. [Limitations & Future Work](#7-limitations--future-work)  
8. [Licence](#8-licence)  
9. [Concluding Remarks](#9-concluding-remarks)  
10. [Live Demo](#10-live-demo)  

---

## 1. Introduction

**RailSecure** is an interactive Streamlit application that demonstrates how a modern, regulation-aware security-awareness programme might look inside a rail operator such as Iarnród Éireann.  
It complements – rather than replaces – the traditional slide-deck presented during the interview by providing **hands-on modules** covering phishing, password hygiene, incident response, compliance, and more.  
All dynamic content (quizzes, scenarios, feedback) is generated in real time with **OpenAI GPT-4o**.

---

## 2. Project Genesis & Objectives

The interview brief:

> *“Explain the cyber-security regulations Irish Rail must abide by, the tools aiding compliance, and how to set up a security-awareness programme.”*

RailSecure was built **to augment my slides** and to:

* **💡 Show innovation** – move beyond theory into an engaging, self-service learning portal.  
* **🛠️ Offer practical tooling** – quizzes, phishing drills, CVE feeds, incident simulations.  
* **📜 Embed compliance context** – NIS2, GDPR, CER Directive, ISO 27001, IEC 62443.  
* **🤖 Leverage AI** – generate bespoke scenarios, auto-mark answers, run live Q&A.  
* **🔐 Demonstrate prompt-engineering controls** – system prompts constrain scope and mitigate jailbreak attempts.  
* **🛡️ Foster security culture** – illustrate how everyone becomes part of the defence-in-depth strategy.

---

## 3. Key Features

| Module | Description |
|--------|-------------|
| **Home** | Welcome, feature overview, Dublin-localised time & version. |
| **Phishing Awareness** | GPT-generated phishing emails, user red-flag analysis with AI feedback, plus “paste-your-own” email inspector. |
| **Password Tools** | Secure password generator, `zxcvbn` strength checker, best-practice tips. |
| **Incident Scenario Simulation** | GPT-crafted IT/OT incident narrative, user response strategy, AI critique. |
| **Incident Response Guides** | Six-phase generic framework + AI-generated scenario-specific guides (NIS2/GDPR timelines). |
| **Compliance Hub** | Expanders on SIEM/SOAR/GRC, IAM, OT monitoring; blueprint for awareness programme; live compliance Q&A. |
| **Cyber-Security Quiz** | GPT-generated MCQs, instant scoring, detailed explanations. |
| **CVE Explainer** | Latest 30-day CVEs pulled from NVD, CVSS v3.1 severity display. |
| **Reference Library** | Curated links to directives & standards, AI explain-it-to-me bot. |
| **Why Awareness Matters** | Gallery of real transport cyber incidents for context. |

All state is managed in `st.session_state` for seamless navigation.

---

## 4. Technology Stack

| Layer | Tech | Notes |
|-------|------|-------|
| **UI** | [Streamlit 1.x](https://streamlit.io) | Custom CSS for dark theme & hero background. |
| **Language** | Python 3.9+ | No external DB required. |
| **LLM** | [OpenAI Python SDK](https://github.com/openai/openai-python) | GPT-4o; temperature tuned per task. |
| **Password Analysis** | [`zxcvbn`](https://github.com/dropbox/zxcvbn) | Crack-time estimation & feedback. |
| **External Data** | NVD CVE API v2 (`requests`) | Live vulnerability feed. |
| **Assets** | Local images for logo/favicon/background. |
| **Deployment** | Streamlit Community Cloud | Free tier; secrets stored per-project. |

---

## 5. Architecture & Code Layout

### 5.1 Directory Tree
```text
.
├── streamlit_app.py         # Entry-point & sidebar router
├── requirements.txt
│
├── assets/
│   ├── background.jpg
│   ├── favicon.png
│   └── logo.png
│
├── utils/
│   ├── helpers.py           # OpenAI client, CSS injector, session init, LLM helpers
│   └── __init__.py
│
└── modules/                 # One file per feature page
    ├── compliance_module.py
    ├── cve_explainer_module.py
    ├── cybersecurity_quiz_module.py
    ├── home_module.py
    ├── incident_response_module.py
    ├── password_module.py
    ├── phishing_module.py
    ├── reference_module.py
    ├── scenario_quiz_module.py
    ├── security_awareness_importance_module.py
    └── __init__.py
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

## 9. Concluding Remarks

Creating RailSecure required blending pedagogy, regulatory insight and code craftsmanship under tight interview timelines.
Prompt-engineering guardrails were a key focus: every GPT call uses explicit system prompts, strict output formats and out-of-scope refusals to reduce jailbreak risk.
The accompanying presentation for this is available in the repository.
I hope the project shows how interactive tools can elevate a standard presentation – and that it sparks ideas for your own awareness programmes.

Feel free to explore, fork and improve!

---

## 10. Live Demo

**▶️ Try the app:** [https://railsecure.streamlit.app](https://railsecure.streamlit.app) 🎉

