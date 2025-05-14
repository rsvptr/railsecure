# modules/compliance_module.py
# This module handles the "Compliance Hub" section of the RailSecure Learning Platform.
# It provides information on compliance tools and technologies, details about
# a security awareness program, and an AI-powered Q&A feature for compliance-related questions.

import streamlit as st
from utils.helpers import create_llm_messages # Helper to structure LLM prompts

# --- Static Content Display Functions ---

def _display_compliance_tools():
    """
    Displays static information about key cybersecurity compliance tools and technologies
    relevant to rail operators, particularly in the context of NIS2 and GDPR.
    Uses expanders for better readability.
    """
    st.markdown("##### Key Compliance Tools & Technologies for Rail Operators")
    st.write(
        "Effective cybersecurity in the rail sector, especially under regulations like NIS2, "
        "requires a robust suite of tools. Here are some critical categories:"
    )

    # Dictionary containing tool categories and their descriptions
    tools_data = {
        "SIEM (Security Information and Event Management)": "Tools like Splunk, IBM QRadar, and Azure Sentinel are crucial. They aggregate logs from both IT and Operational Technology (OT) systems, enabling continuous monitoring, threat detection, and rapid incident analysis – a cornerstone of NIS2 compliance for essential services.",
        "SOAR (Security Orchestration, Automation, and Response)": "Solutions such as Palo Alto Cortex XSOAR and IBM Resilient automate incident response workflows. This ensures structured notifications and actions, helping meet strict reporting timelines (e.g., 24-hour initial NIS2 reporting).",
        "GRC Platforms (Governance, Risk & Compliance)": "Platforms like RSA Archer, ServiceNow GRC, and MetricStream help map legal obligations (NIS2, GDPR, CER Directive) to internal controls, track compliance status, manage risk assessments, and provide real-time dashboards for oversight.",
        "Vulnerability Management": "Tools like Tenable Nessus, QualysGuard, and Rapid7 InsightVM continuously scan IT/OT networks for vulnerabilities. This proactive approach is essential for timely patching and risk mitigation, as mandated by risk management obligations in NIS2.",
        "Intrusion Detection/Prevention Systems (IDS/IPS) & EDR/XDR": "Systems from vendors like CrowdStrike, Microsoft Defender for Endpoint, and specialized OT monitoring solutions (e.g., Nozomi Networks, Claroty) detect anomalous activity, prevent lateral movement, and provide endpoint/extended detection and response capabilities.",
        "Identity and Access Management (IAM) & Privileged Access Management (PAM)": "Solutions like Okta, Azure AD, and CyberArk enforce multi-factor authentication (MFA), least-privilege access, and secure management of privileged accounts. These are critical for both GDPR data protection and NIS2 security requirements.",
        "Data Loss Prevention (DLP) & Encryption": "DLP systems and robust encryption tools (for data-at-rest and data-in-transit) are vital for safeguarding sensitive customer data (GDPR) and critical operational information. This includes protecting data on legacy systems where feasible.",
        "OT Security Monitoring": "Specialized tools designed for Industrial Control Systems (ICS) environments are essential for monitoring traffic, detecting threats specific to OT protocols, and ensuring the resilience of rail signalling and control systems."
    }

    # Display each tool category and its description in an expander
    for tool, description in tools_data.items():
        with st.expander(f"**{tool}**"):
            st.markdown(description)

def _display_security_awareness_program():
    """
    Displays static information outlining the essential elements of a comprehensive
    security awareness program for an organization like Iarnród Éireann.
    """
    st.markdown("##### Building a Culture of Security: Awareness Program Essentials")
    st.write(
        "A strong security awareness program is a key defense layer, mandated by regulations like NIS2, "
        "and crucial for protecting Iarnród Éireann."
    )
    
    # Detailed markdown content describing objectives, content areas, delivery methods, and success metrics
    st.markdown(
        """
        **Core Objectives:**
        * **Reduce Human Error:** Minimize risky behaviors like falling for phishing, using weak passwords, or mishandling sensitive data.
        * **Protect Critical Assets:** Safeguard Iarnród Éireann's critical IT and OT systems, operational data, and customer information in line with GDPR and NIS2.
        * **Foster Vigilance:** Cultivate a proactive security culture where all staff feel responsible for cybersecurity.
        * **Ensure Compliance:** Meet regulatory requirements for staff training and awareness.

        **Key Programme Content Areas:**
        * **Foundational Training (All Staff):**
            * Phishing and social engineering recognition (with practical examples).
            * Strong password creation and management (including password manager advocacy).
            * Safe internet use and secure handling of removable media.
            * Identifying and reporting security incidents promptly.
            * Understanding data protection principles (GDPR basics).
        * **Role-Specific Modules:**
            * **IT & OT Staff:** Advanced threat detection, secure coding (if applicable), specific OT security protocols, incident response procedures.
            * **Managers & Executives:** Understanding cyber risk, crisis communication, compliance responsibilities under NIS2/GDPR.
            * **Data Handling Personnel (e.g., HR, Finance, Customer Service):** Specific training on GDPR, secure data handling, and privacy-enhancing techniques for their roles.
        * **Regular Updates & Refreshers:**
            * Current threat landscape (new ransomware tactics, emerging phishing techniques).
            * Lessons learned from internal or industry incidents.
            * Updates to Iarnród Éireann's security policies and procedures.

        **Effective Delivery Methods:**
        * **Interactive E-Learning:** Engaging modules with quizzes, videos, and simulations.
        * **Targeted Workshops & Briefings:** For specific roles or departments.
        * **Phishing Simulation Campaigns:** Regular, unannounced tests to gauge awareness and identify areas for improvement.
        * **Internal Communications:** Newsletters, intranet articles, posters, security champions network.
        * **Gamification:** Leaderboards, points, or badges for completing training or reporting threats (use judiciously).

        **Measuring Success & Continuous Improvement:**
        * **Completion Rates:** Track participation in mandatory training.
        * **Quiz & Simulation Performance:** Assess understanding and detection capabilities.
        * **Incident Reporting Trends:** Monitor the number and quality of user-reported incidents (an increase in good reports can be positive).
        * **User Feedback:** Surveys and direct feedback to refine program content and delivery.
        * **Periodic Audits & Assessments:** Evaluate overall program effectiveness against objectives and compliance needs.
        """
    )

# --- AI-Powered Q&A Function ---

def _ask_compliance_query_gpt(openai_client, user_query):
    """
    Uses the OpenAI API to answer a user's query related to cybersecurity compliance
    and security awareness, specifically tailored for Iarnród Éireann.

    Args:
        openai_client (openai.OpenAI): The initialized OpenAI client.
        user_query (str): The user's question.

    Returns:
        str: The AI's generated answer, or an error message if the query fails.
    """
    # System prompt defining the AI's role, expertise, and response guidelines
    system_prompt = (
        "You are an expert AI assistant specializing in cybersecurity compliance and security awareness, specifically for Iarnród Éireann (Irish Rail). "
        "Your knowledge covers NIS2 Directive, GDPR, the Irish Data Protection Act of 2018, the CER Directive, and general rail transport security best practices. "
        "Provide concise, accurate, and practical answers to user queries. "
        "If a query is outside this defined scope (e.g., asking for general IT help, unrelated topics), politely state: "
        "'This query falls outside my expertise in cybersecurity compliance and rail security. Please ask a question related to NIS2, GDPR, the Irish Data Protection Act 2018, CER, or security practices within Iarnród Éireann.' "
        "Do not invent information. If you are unsure about a very specific internal Iarnród Éireann policy detail, state that and recommend checking internal documentation or contacting the relevant department. "
        "Focus on providing helpful information that aligns with regulatory requirements and industry best practices for a rail operator."
    )
    # The user's query is passed directly as the user prompt content
    user_prompt = user_query

    try:
        # Make the API call to OpenAI
        response = openai_client.chat.completions.create(
            model="gpt-4o", # Specify the model
            messages=create_llm_messages(system_prompt, user_prompt), # Formatted messages
            temperature=0.3, # Lower temperature for more factual and concise answers
            max_tokens=600   # Max length of the response
        )
        # Return the AI's response text
        return response.choices[0].message.content.strip()
    except Exception as e:
        # Handle any errors during the API call
        st.error(f"Error processing compliance query: {e}")
        return "Error: Could not get an answer for your compliance query."

# --- Main Display Function for the Module ---

def display_compliance_hub(openai_client):
    """
    Displays the main UI for the Compliance Hub module.
    It uses tabs to organize content for tools, awareness programs, and AI Q&A.

    Args:
        openai_client (openai.OpenAI or None): The initialized OpenAI client.
                                               If None, AI Q&A features will be disabled.
    """
    st.subheader("🏛️ Compliance Hub: Tools, Programs & Q&A")
    st.write(
        "Navigate through essential information on compliance tools, security awareness program components, "
        "and get AI-powered answers to your compliance-related questions relevant to Iarnród Éireann."
    )

    # Create tabs for different sections of the compliance hub
    tab1, tab2, tab3 = st.tabs([
        "⚙️ Compliance Tools & Technologies", 
        "👥 Security Awareness Program", 
        "🤖 Ask the Compliance AI"
    ])

    # Content for the "Compliance Tools & Technologies" tab
    with tab1:
        _display_compliance_tools()

    # Content for the "Security Awareness Program" tab
    with tab2:
        _display_security_awareness_program()

    # Content for the "Ask the Compliance AI" tab
    with tab3:
        st.markdown("#### Interactive Compliance Q&A")
        st.write(
            "Have a question about cybersecurity tools, NIS2, GDPR, the Irish Data Protection Act 2018, "
            "the CER Directive, or general rail security best practices at Iarnród Éireann? Ask below."
        )
        
        if not openai_client:
            # Display a warning if the OpenAI client isn't available
            st.warning("The AI Q&A feature is currently unavailable as the OpenAI client could not be initialized. Please check API key configuration.")
        else:
            # Input field for the user's query
            user_query = st.text_input(
                "Enter your compliance or security awareness question:", 
                key="compliance_query_input", # Unique key for the input widget
                placeholder="e.g., What are key requirements of NIS2 for reporting incidents?"
            )

            # Button to submit the query
            if st.button("💬 Get AI Insight", key="ask_compliance_ai"):
                if not user_query.strip(): # Check if the query is empty
                    st.warning("Please enter your question before submitting.")
                else:
                    # Show a spinner while waiting for the AI response
                    with st.spinner("Consulting compliance knowledge base..."):
                        answer = _ask_compliance_query_gpt(openai_client, user_query)
                        # Store the answer in session state to persist it
                        st.session_state["compliance_query_answer"] = answer
            
            # Display the AI's answer if it exists in session state
            if st.session_state.get("compliance_query_answer"):
                st.markdown("---") # Visual separator
                st.markdown("##### AI Response:")
                st.info(st.session_state["compliance_query_answer"]) # Display answer in an info box
