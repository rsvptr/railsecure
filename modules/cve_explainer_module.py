# modules/cve_explainer_module.py
# This module is responsible for fetching and displaying the latest Common
# Vulnerabilities and Exposures (CVEs) from the National Vulnerability Database (NVD).
# It helps users stay informed about recent software vulnerabilities.

import streamlit as st
import requests                     # For making HTTP requests to the NVD API
from datetime import datetime, timedelta # For handling dates, e.g., fetching CVEs from a recent period

# --- Helper Function for CVSS Data ---

def _get_cvss_v3_details(metrics):
    """
    Extracts CVSS V3.1 base score, severity, and vector string from CVE metrics data.

    Args:
        metrics (dict): The 'metrics' part of a CVE object from the NVD API response.

    Returns:
        tuple: (base_score, severity, vector_string) or (None, None, None) if not found.
    """
    # Check if CVSS V3.1 metrics are present
    if "cvssMetricV31" in metrics and metrics["cvssMetricV31"]:
        # NVD API often returns cvssMetricV31 as a list, take the first element
        cvss_data_container = metrics["cvssMetricV31"][0]
        cvss_data = cvss_data_container.get("cvssData", {}) # Get the actual CVSS data
        
        base_score = cvss_data.get("baseScore")
        severity = cvss_data.get("baseSeverity")
        vector_string = cvss_data.get("vectorString")
        return base_score, severity, vector_string
    return None, None, None # Return None if CVSS V3.1 data is not available

# --- CVE Fetching Function ---

def _fetch_latest_cves(api_key=None, count=5):
    """
    Fetches a specified number of the most recently published CVEs from the NVD API.

    It queries for CVEs published in the last 30 days and sorts them to get the
    most recent ones.

    Args:
        api_key (str, optional): An NVD API key for potentially higher rate limits. Defaults to None.
        count (int, optional): The number of latest CVEs to fetch. Defaults to 5.

    Returns:
        list or None: A list of CVE vulnerability items if successful, otherwise None.
                      Displays errors in Streamlit on failure.
    """
    base_url = "https://services.nvd.nist.gov/rest/json/cves/2.0/" # NVD CVE API v2.0 endpoint
    headers = {}
    if api_key: # Add API key to headers if provided
        headers['apiKey'] = api_key

    # To get the most recently published, query for CVEs published in a recent window (e.g., last 30 days)
    # and fetch a slightly larger set to sort locally for the actual 'count' latest.
    end_date = datetime.utcnow() # Current UTC time
    start_date = end_date - timedelta(days=30) # Look back 30 days
    
    params = {
        "pubStartDate": start_date.strftime('%Y-%m-%dT%H:%M:%SZ'), # Format for NVD API
        "pubEndDate": end_date.strftime('%Y-%m-%dT%H:%M:%SZ'),
        "resultsPerPage": 20 # Fetch more than 'count' to ensure we get enough recent ones after sorting
    }

    try:
        # Make the GET request to the NVD API
        response = requests.get(base_url, params=params, headers=headers, timeout=10) # 10-second timeout
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        data = response.json()      # Parse the JSON response
        
        vulnerabilities = data.get("vulnerabilities", []) # Get the list of vulnerabilities
        
        # Sort the fetched vulnerabilities by their publication date in descending order
        # to ensure the latest ones are first.
        if vulnerabilities:
            vulnerabilities.sort(key=lambda x: x.get('cve', {}).get('published', ''), reverse=True)
        
        # Return the top 'count' vulnerabilities from the sorted list
        return vulnerabilities[:count]
        
    except requests.exceptions.RequestException as e:
        # Handle network-related errors or bad HTTP responses
        st.error(f"Failed to fetch CVEs from NVD: {e}")
        return None
    except ValueError: # Includes JSONDecodeError if response is not valid JSON
        st.error("Failed to parse CVE data from NVD.")
        return None

# --- Main Display Function for the Module ---

def display_cve_explainer(nvd_api_key=None):
    """
    Displays the main UI for the CVE Explainer module.
    It fetches and lists the latest CVEs with their summaries and CVSS scores.

    Args:
        nvd_api_key (str, optional): The NVD API key, passed from the main app.
    """
    st.subheader("⚠️ Latest CVE Insights from NVD")
    st.write(
        "Stay informed about the latest Common Vulnerabilities and Exposures (CVEs). Understanding these vulnerabilities "
        "is crucial for protecting Iarnród Éireann's systems. Information is sourced from the "
        "[National Vulnerability Database (NVD)](https://nvd.nist.gov/)."
    )
    
    # Display the current time for context on data freshness
    current_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S %Z') # Uses server's local timezone
    st.caption(f"Data fetched based on publications up to: {current_date_time}")

    # Button to manually refresh the CVE list
    if st.button("🔄 Refresh Latest CVEs", key="refresh_cves_button"):
        # The fetch operation is called directly below, so this button primarily triggers a rerun.
        # If caching were implemented, this button would clear the cache.
        pass 

    # Fetch the latest CVEs
    latest_cves = _fetch_latest_cves(api_key=nvd_api_key, count=5)

    if latest_cves: # If CVE data was successfully fetched
        st.markdown(f"#### Displaying up to 5 most recently published CVEs:")
        # Provide a legend for CVSS severity scores for user reference
        st.markdown("""
        **CVSS Severity Scale:**
        * **None:** 0.0
        * **Low:** 0.1 - 3.9
        * **Medium:** 4.0 - 6.9
        * **High:** 7.0 - 8.9
        * **Critical:** 9.0 - 10.0
        """)
        st.markdown("---") # Visual separator

        # Iterate through the fetched CVEs and display their details
        for index, vulnerability_item in enumerate(latest_cves):
            cve_data = vulnerability_item.get("cve", {}) # The main CVE object
            cve_id = cve_data.get("id", "N/A")           # CVE identifier (e.g., CVE-2023-XXXXX)
            
            # Extract English description
            descriptions = cve_data.get("descriptions", [])
            summary = "No English summary available."
            for desc in descriptions:
                if desc.get("lang") == "en":
                    summary = desc.get("value", summary)
                    break
            
            # Format the publication date
            published_date_str = cve_data.get("published", "N/A")
            if published_date_str != "N/A":
                try:
                    # Convert ISO format string to a readable date-time string
                    published_date_display = datetime.fromisoformat(published_date_str.replace("Z", "+00:00")).strftime('%Y-%m-%d %H:%M:%S %Z')
                except ValueError:
                    published_date_display = published_date_str # Fallback to raw string if parsing fails
            else:
                published_date_display = "N/A"

            # Get CVSS V3.1 details using the helper function
            base_score_v3, severity_v3, vector_v3 = _get_cvss_v3_details(cve_data.get("metrics", {}))

            # Display each CVE in a bordered container for better visual grouping
            with st.container(border=True):
                st.markdown(f"##### {index + 1}. **{cve_id}**") # Numbered CVE entry with ID
                st.markdown(f"**Published:** {published_date_display}")
                
                # Display CVSS score and severity if available
                if base_score_v3 is not None and severity_v3:
                    st.markdown(f"**CVSS v3.1 Score:** `{base_score_v3}` (**{severity_v3}**)")
                    if vector_v3: # Display vector string if present
                        st.caption(f"Vector: `{vector_v3}`")
                else:
                    st.markdown("**CVSS v3.1 Score:** `Not Available`")

                # Use an expander for the detailed summary to save space
                with st.expander("View Summary/Description"):
                    st.markdown(summary if summary else "No detailed summary provided.")
                
                # Link to the official NVD page for the CVE
                st.markdown(f"[More Details on NVD](https://nvd.nist.gov/vuln/detail/{cve_id})")
            st.markdown("---") # Separator for the next CVE entry
            
    elif latest_cves is None: # Explicit check for None (indicates an error during fetch)
        st.error("Could not retrieve CVE information at this time. Please try again later or check the NVD website directly.")
    else: # If latest_cves is an empty list (no error, but no data)
        st.info("No new CVEs found matching the criteria in the last 30 days, or the NVD service returned no results.")
