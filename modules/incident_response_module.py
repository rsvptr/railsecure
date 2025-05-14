# modules/incident_response_module.py
# This module provides the "Incident Response Guides" feature for the platform.
# It includes a static general incident response framework and allows users to
# generate custom, scenario-specific incident response guides using an LLM.

import streamlit as st
from utils.helpers import create_llm_messages # Helper to structure LLM prompts

# --- Static Content Display Function ---

def _display_general_incident_response_guide():
    """
    Displays a comprehensive, general incident response guide.
    The guide outlines key phases: Preparation, Identification, Containment,
    Eradication, Recovery, and Post-Incident Analysis, along with regulatory
    pointers and best practices relevant to Iarnród Éireann.
    """
    st.markdown("#### Core Phases of Incident Response")
    st.write(
        """
        A structured approach to incident response is vital for minimizing impact and ensuring rapid recovery. 
        The following steps outline a general framework applicable to Iarnród Éireann, aligning with industry best practices 
        and regulatory expectations like NIS2 and GDPR.
        """
    )

    # Dictionary defining the phases of incident response and their descriptions
    phases = {
        "1. Preparation": "This proactive phase involves establishing an incident response plan, forming a dedicated response team (with clear roles and responsibilities), acquiring necessary tools (SIEM, EDR, forensics tools), conducting regular training and drills, and assessing risks to critical systems (both IT and OT).",
        "2. Identification": "Detecting and verifying an incident. This involves continuous monitoring via SIEM, IDS/IPS, EDR systems, and OT monitoring tools. Key activities include analyzing alerts, recognizing anomalies (e.g., unusual network traffic, unauthorized access attempts, system malfunctions), and initial incident assessment (scoping, severity). User reports are also crucial here.",
        "3. Containment": "Limiting the scope and impact of the incident. Short-term containment might involve isolating affected network segments, blocking malicious IP addresses, or disabling compromised accounts. Long-term containment focuses on more robust measures while eradication strategies are developed.",
        "4. Eradication": "Removing the threat actor and malicious components from the environment. This includes eliminating malware, remediating vulnerabilities that were exploited, and ensuring no backdoors remain. For OT systems, this requires careful coordination to maintain operational safety.",
        "5. Recovery": "Restoring affected systems and services to normal operation securely. This involves restoring from clean backups, validating system integrity, monitoring for any signs of reinfection, and a phased return to service. For rail operations, safety and service continuity are paramount.",
        "6. Post-Incident Analysis (Lessons Learned)": "A critical phase conducted after the incident is resolved. It involves a detailed review to understand the root cause, the effectiveness of the response, and areas for improvement. Document findings, update the incident response plan, refine security controls, and share lessons with relevant stakeholders. This feeds back into the Preparation phase."
    }

    # Display each phase and its description in an expander for better UI organization
    for phase, description in phases.items():
        with st.expander(f"**{phase}**"):
            st.markdown(description)

    st.markdown("---") # Visual separator
    st.markdown("#### Key Regulatory Pointers & Best Practices")
    # Information on regulatory reporting timelines and general best practices
    st.markdown(
        """
        * **NIS2 Directive:** Significant incidents impacting essential services (like rail transport) must be reported to the National Cyber Security Centre (NCSC) with an early warning within **24 hours** of becoming aware, and a detailed notification within **72 hours**. A final report is typically due within one month.
        * **GDPR (General Data Protection Regulation):** Personal data breaches must be reported to the Data Protection Commission (DPC) within **72 hours** of becoming aware, unless the breach is unlikely to result in a risk to individuals' rights and freedoms. Affected individuals may also need to be notified.
        * **Preserve Evidence:** Maintain detailed logs and forensic evidence throughout the response process for internal analysis, regulatory reporting, and potential legal action.
        * **Communication Plan:** Have a clear internal and external communication plan. This includes notifying management, legal teams, PR, and potentially customers or the public, depending on the incident's nature and severity.
        * **Regular Drills:** Conduct tabletop exercises and full simulation drills to test your incident response plan and team readiness.
        * **IT/OT Convergence:** Pay special attention to incidents that may span both IT and Operational Technology (OT) environments, ensuring response strategies consider the unique safety and operational requirements of OT systems in rail.
        """
    )

# --- LLM Interaction for Custom Guide Generation ---

def _generate_custom_incident_response_guide_gpt(openai_client, category):
    """
    Generates a custom, detailed incident response guide for a given scenario category
    using an OpenAI model, tailored specifically for Iarnród Éireann.

    Args:
        openai_client (openai.OpenAI): The initialized OpenAI client.
        category (str): The category of the incident for which the guide is needed.

    Returns:
        str: A string containing the generated custom incident response guide,
             or an error message if generation fails.
    """
    # System prompt defining the AI's role, expertise, and desired output structure/content
    system_prompt = (
        "You are a senior cybersecurity incident response planner, specializing in the rail transport sector, specifically for Iarnród Éireann. "
        "Your task is to generate a detailed, step-by-step incident response guide for the specified scenario category. "
        "The guide must be structured around standard incident response phases: Preparation (briefly, as it's ongoing), Identification, Containment, Eradication, Recovery, and Post-Incident Analysis (Lessons Learned). "
        "For each phase, provide actionable steps relevant to the chosen scenario and Iarnród Éireann's context (considering both IT and OT systems where applicable). "
        "Explicitly mention relevant Irish/EU regulatory requirements (e.g., NIS2 reporting timelines, GDPR breach notifications) and best practices for handling the specific type of incident. "
        "The guide must be realistic, comprehensive, scenario-specific, and practical for Iarnród Éireann staff. "
        "Ensure your output is formatted clearly as a guide. Do not include any conversational fluff or commentary outside the guide itself. Your entire response must be the guide content."
    )
    user_prompt = f"Generate a custom incident response guide for Iarnród Éireann for the following incident category: {category}."

    try:
        # API call to OpenAI to generate the custom guide
        response = openai_client.chat.completions.create(
            model="gpt-4o", # Specify the model
            messages=create_llm_messages(system_prompt, user_prompt), # Formatted messages
            temperature=0.6,  # Temperature for balanced creativity and factualness
            max_tokens=1200   # Allow sufficient tokens for a detailed guide
        )
        # Return the AI's generated text
        return response.choices[0].message.content.strip()
    except Exception as e:
        # Handle errors during the API call
        st.error(f"Error generating custom incident response guide: {e}")
        return "Error: Could not generate the custom guide."

# --- Main Display Function for the Module ---

def display_incident_response_guide(openai_client):
    """
    Displays the main UI for the Incident Response Guides module.
    It uses tabs to separate the general framework from the custom guide generator.

    Args:
        openai_client (openai.OpenAI or None): The initialized OpenAI client.
                                               If None, custom guide generation will be disabled.
    """
    st.subheader("📖 Incident Response Guides")
    st.write(
        "Access general incident response steps and generate custom guides tailored to specific "
        "cybersecurity scenarios relevant to Iarnród Éireann."
    )

    # Create tabs for different sections
    tab1, tab2 = st.tabs([
        "📜 General Incident Response Framework", 
        "🛠️ Custom Scenario-Specific Guide"
    ])

    # Content for the "General Incident Response Framework" tab
    with tab1:
        _display_general_incident_response_guide()

    # Content for the "Custom Scenario-Specific Guide" tab
    with tab2:
        st.markdown("#### Generate a Custom Incident Response Guide")
        st.write(
            "Select an incident category below to generate a more detailed, scenario-specific response guide "
            "tailored for Iarnród Éireann's environment."
        )

        if not openai_client:
            # Display a warning if OpenAI client is not available for this feature
            st.warning("The custom guide generation feature is currently unavailable as the OpenAI client could not be initialized.")
        else:
            # Categories for which custom guides can be generated
            scenario_categories_for_guides = [
                "Ransomware Attack on Critical Systems",
                "Major Data Breach (Customer/Employee PII)",
                "Targeted Attack on Rail Signalling (OT System)",
                "Compromise of Cloud Services (e.g., Ticketing Platform)",
                "Widespread Phishing Leading to Multiple Account Breaches",
                "Insider Threat Data Exfiltration",
                "Denial-of-Service Attack Affecting Operations"
            ]
            # Dropdown for user to select an incident category
            selected_category = st.selectbox(
                "Select an Incident Scenario Category for Your Custom Guide:",
                options=scenario_categories_for_guides,
                index=0, # Default selection
                key="custom_guide_category_selector", # Unique key for the widget
                help="The chosen category will shape the specifics of the generated response guide."
            )

            # Button to trigger custom guide generation
            if st.button("Generate Custom Response Guide", key="generate_custom_ir_guide_button"):
                with st.spinner(f"Generating custom response guide for '{selected_category}'..."):
                    custom_guide_text = _generate_custom_incident_response_guide_gpt(openai_client, selected_category)
                    # Store the generated guide in session state
                    st.session_state["custom_incident_guide"] = custom_guide_text
            
            # Display the generated custom guide if it exists in session state
            if st.session_state.get("custom_incident_guide"):
                st.markdown("---") # Visual separator
                st.markdown("##### Your Custom Incident Response Guide:")
                with st.container(border=True): # Display in a bordered container
                    st.markdown(st.session_state["custom_incident_guide"])
