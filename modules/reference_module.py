# modules/reference_module.py
# This module provides the "Regulatory & Best Practice References" section.
# It offers a curated list of useful links to official documentation and standards,
# and an AI-powered Q&A feature for specific queries on these topics, tailored
# for Iarnród Éireann.

import streamlit as st
from utils.helpers import create_llm_messages # Helper to structure LLM prompts

# --- Static Content Display Function ---

def _display_key_reference_links():
    """
    Displays a curated list of key cybersecurity and regulatory reference links,
    categorized for easier navigation. Each link includes a title, URL, and a brief description.
    """
    st.markdown("#### Essential Cybersecurity & Regulatory References")
    st.write(
        "Below is a collection of important resources for understanding cybersecurity directives, "
        "data protection laws, and industry standards relevant to Iarnród Éireann."
    )

    # Dictionary structure to hold categorized reference links
    references = {
        "EU Directives & Regulations": [
            {
                "title": "NIS2 Directive Overview (Official EU Site)", 
                "url": "https://digital-strategy.ec.europa.eu/en/policies/nis2-directive",
                "desc": "The primary EU legislation on cybersecurity for essential and important entities."
            },
            {
                "title": "Critical Entities Resilience (CER) Directive",
                "url": "https://www.consilium.europa.eu/en/press/press-releases/2022/12/08/council-adopts-new-rules-to-enhance-the-resilience-of-critical-entities/",
                "desc": "Complements NIS2 by focusing on the physical resilience of critical entities."
            },
            {
                "title": "What is GDPR? (Official EU GDPR Portal)", 
                "url": "https://gdpr.eu/what-is-gdpr/",
                "desc": "Comprehensive information on the General Data Protection Regulation."
            },
            {
                "title": "ENISA (EU Agency for Cybersecurity) - Transport Sector Reports",
                "url": "https://www.enisa.europa.eu/topics/critical-information-infrastructures-and-services/nis-directive/sectoral-information/transport",
                "desc": "Specific guidance and reports for the transport sector from ENISA."
            }
        ],
        "Irish Legislation & Guidance": [
            {
                "title": "NCSC Ireland - NIS2 Guide", 
                "url": "https://www.ncsc.gov.ie/pdfs/NCSC_NIS2_Guide.pdf", # User should verify link currency
                "desc": "Guidance from Ireland's National Cyber Security Centre on NIS2."
            },
            {
                "title": "Irish Data Protection Act 2018 (Official Legislation)", 
                "url": "https://www.irishstatutebook.ie/eli/2018/act/7/enacted/en/html",
                "desc": "The Irish law that incorporates and further specifies aspects of GDPR."
            },
            {
                "title": "Data Protection Commission (DPC) Ireland - GDPR Overview", 
                "url": "https://www.dataprotection.ie/en/organisations/know-your-obligations/what-gdpr",
                "desc": "Guidance and resources from Ireland's data protection authority."
            }
        ],
        "Industry Standards & Best Practices": [
            {
                "title": "ISO/IEC 27001 - Information Security Management", 
                "url": "https://www.iso.org/isoiec-27001-information-security.html",
                "desc": "International standard for information security management systems (ISMS)."
            },
            {
                "title": "IEC 62443 - Security for Industrial Automation and Control Systems", 
                "url": "https://www.isa.org/standards-and-publications/isa-standards/isa-iec-62443-series-of-standards",
                "desc": "Key series of standards for Operational Technology (OT) cybersecurity, highly relevant for rail."
            },
             {
                "title": "NIST Cybersecurity Framework",
                "url": "https://www.nist.gov/cyberframework",
                "desc": "A popular framework for improving critical infrastructure cybersecurity."
            }
        ]
    }

    # Iterate through categories and links, displaying them using markdown
    for category, links in references.items():
        st.markdown(f"##### {category}") # Category header
        for link_info in links:
            # Format each link as: * **[Title](URL)** \n    *Description*
            st.markdown(f"* **[{link_info['title']}]({link_info['url']})** \n    *_{link_info['desc']}_*")
        st.markdown("---") # Separator after each category

# --- AI-Powered Q&A Function ---

def _ask_llm_reference_gpt(openai_client, user_query):
    """
    Uses an OpenAI model to answer user queries about cybersecurity regulations,
    standards, and best practices, tailored to the Iarnród Éireann context.

    Args:
        openai_client (openai.OpenAI): The initialized OpenAI client.
        user_query (str): The user's question.

    Returns:
        str: The AI's generated answer, or an error message if the query fails.
    """
    # System prompt defining the AI's role, expertise, and response guidelines.
    # Includes instructions for handling out-of-scope queries.
    system_prompt = (
        "You are an expert AI assistant specializing in European and Irish cybersecurity directives (NIS2, GDPR, Irish Data Protection Act 2018, CER Directive) "
        "and relevant rail transport security standards (e.g., ISO 27001, IEC 62443 in the context of rail operations) for Iarnród Éireann. "
        "Your role is to provide concise, accurate, and helpful answers to queries. When appropriate, you can refer to official guidelines or specific clauses if known. "
        "If a query is too vague, ask for clarification. If it's clearly out of scope (e.g., asking for non-cybersecurity legal advice or train schedules), "
        "politely state: 'This query falls outside my expertise in cybersecurity regulations and rail security standards. Please ask a question related to these topics for Iarnród Éireann.' "
        "Prioritize information directly applicable to Iarnród Éireann's context. Do not invent information. If unsure about a very specific internal policy, state that and advise checking official internal documentation."
    )
    user_prompt = user_query # The user's query is passed as the user message content

    try:
        # API call to OpenAI
        response = openai_client.chat.completions.create(
            model="gpt-4o", # Specify the model
            messages=create_llm_messages(system_prompt, user_prompt), # Formatted messages
            temperature=0.2, # Low temperature for more factual and precise answers
            max_tokens=800   # Max length for the response
        )
        # Return the AI's response text
        return response.choices[0].message.content.strip()
    except Exception as e:
        # Handle errors during the API call
        st.error(f"Error processing reference query: {e}")
        return "Error: Could not get an answer for your reference query."

# --- Main Display Function for the Module ---

def display_reference_materials(openai_client):
    """
    Displays the main UI for the Reference Materials module.
    It uses tabs to separate the list of key reference links from the AI Q&A feature.

    Args:
        openai_client (openai.OpenAI or None): The initialized OpenAI client.
                                               If None, AI Q&A features will be disabled.
    """
    st.subheader("📚 Regulatory & Best Practice References")
    st.write(
        "Access key reference documents and ask our AI for explanations regarding cybersecurity regulations, "
        "data protection laws, and industry standards pertinent to Iarnród Éireann."
    )

    # Create tabs for different sections
    tab1, tab2 = st.tabs([
        "🔗 Key Reference Links", 
        "🤖 Ask the Reference AI"
    ])

    # Content for the "Key Reference Links" tab
    with tab1:
        _display_key_reference_links()

    # Content for the "Ask the Reference AI" tab
    with tab2:
        st.markdown("#### Interactive Reference Q&A")
        st.write(
            "Ask about NIS2, GDPR, the Irish Data Protection Act 2018, the CER Directive, "
            "rail security standards (like ISO 27001 or IEC 62443 sections), or specific clauses relevant to Iarnród Éireann."
        )
        
        if not openai_client:
            # Display warning if OpenAI client is not available
            st.warning("The AI Q&A feature is currently unavailable as the OpenAI client could not be initialized.")
        else:
            # Input field for user's query
            user_query = st.text_input(
                "Enter your question about regulations or standards:", 
                key="reference_material_query_input", # Unique key for the widget
                placeholder="e.g., What are the main security measures required under NIS2 Article 21?"
            )

            # Button to submit the query
            if st.button("💬 Get AI Explanation", key="ask_reference_material_ai"):
                if not user_query.strip(): # Check if query is empty
                    st.warning("Please enter your question before submitting.")
                else:
                    # Show spinner while waiting for AI response
                    with st.spinner("Searching relevant directives and standards..."):
                        answer = _ask_llm_reference_gpt(openai_client, user_query)
                        # Store answer in session state
                        st.session_state["reference_query_answer"] = answer
            
            # Display AI's answer if it exists in session state
            if st.session_state.get("reference_query_answer"):
                st.markdown("---") # Visual separator
                st.markdown("##### AI Explanation:")
                # Display response in a bordered container using markdown for rich formatting
                with st.container(border=True):
                    st.markdown(st.session_state["reference_query_answer"])
