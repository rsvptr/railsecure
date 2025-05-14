# modules/security_awareness_importance_module.py
# This module displays content emphasizing the critical role of security awareness
# for Iarnród Éireann staff. It includes illustrative examples of notable cyber
# incidents from the broader transport sector to highlight potential impacts.

import streamlit as st

def display_importance_of_security_awareness():
    """
    Displays the content for the "Why Security Awareness Matters" module.
    This includes an introduction, a list of notable cybersecurity incidents
    in the transport sector (each in an expander), and a concluding message
    emphasizing collective responsibility at Iarnród Éireann.
    """
    st.subheader("🛡️ The Critical Role of Security Awareness at Iarnród Éireann")
    
    # Introductory text on the importance of cybersecurity awareness
    st.markdown(
        """
        In today's interconnected world, the rail and wider transportation sectors are increasingly targeted by sophisticated cyber threats. 
        These threats aren't just digital inconveniences; they can cause significant operational disruption, lead to substantial financial losses, 
        damage public trust, and even compromise passenger and staff safety. At Iarnród Éireann, where the reliability and security of our services 
        are paramount, fostering a strong culture of cybersecurity awareness among all staff is not just beneficial—it's essential.

        Understanding the potential impact of cyber incidents, and learning from real-world examples, helps us all appreciate the importance 
        of our individual roles in protecting our organisation.
        """
    )

    st.markdown("---") # Visual separator
    st.markdown("#### Learning from Past Incidents in the Transport Sector")
    st.write(
        "The following examples from the global rail and broader transport industries highlight the diverse nature of cyber threats and their "
        "far-reaching consequences. While not all directly involve Iarnród Éireann, they offer valuable lessons for us all."
    )

    # List of dictionaries, each representing a notable cyber incident
    incidents = [
        {
            "title": "NotPetya Attack on A.P. Møller-Maersk (June 2017, Global Shipping)",
            "description": (
                "A devastating NotPetya malware attack crippled Maersk’s global IT systems, leading to the shutdown of operations "
                "at 76 port terminals worldwide. The estimated financial impact was between **$200–$300 million**. This incident starkly "
                "demonstrated how cyberattacks can ripple through global supply chains, impacting both digital operations and physical logistics."
            ),
            "link_text": "Read more (Los Angeles Times)",
            "url": "https://www.latimes.com/business/la-fi-maersk-cyberattack-20170817-story.html"
        },
        {
            "title": "Colonial Pipeline Ransomware Attack (May 2021, USA)",
            "description": (
                "A ransomware attack forced Colonial Pipeline to shut down its entire pipeline network, which supplied nearly half of the U.S. "
                "East Coast's fuel. This resulted in widespread fuel shortages and panic buying. A ransom of approximately **$4.4 million** "
                "was paid. The incident underscored the vulnerability of critical national infrastructure."
            ),
            "link_text": "Read more (Reuters)",
            "url": "https://www.reuters.com/technology/colonial-pipeline-ceo-tells-senate-cyber-defenses-were-compromised-by-password-2021-06-08/"
        },
        {
            "title": "Ransomware Attack on Trenitalia (March 2022, Italy)",
            "description": (
                "Italy’s national railway operator, Trenitalia, suffered a significant ransomware attack that disrupted ticketing and reservation systems "
                "for several days. This impacted thousands of passengers and forced the suspension of various digital services until systems could be safely restored."
            ),
            "link_text": "Read more (Bleeping Computer)", 
            "url": "https://www.bleepingcomputer.com/news/security/italian-state-railways-ferrovie-dello-stato-hit-by-ransomware/"
        },
        {
            "title": "Supply-Chain Cyberattack on DSB National Railway (October 2022, Denmark)",
            "description": (
                "A cyberattack targeting a third-party IT subcontractor led to a nationwide shutdown of critical IT applications for Danish State Railways (DSB). "
                "As a direct consequence, all DSB trains were halted for several hours, illustrating how vulnerabilities in the supply chain can severely disrupt transport networks."
            ),
            "link_text": "Read more (Reuters)",
            "url": "https://www.reuters.com/technology/danish-train-standstill-saturday-caused-by-cyber-attack-2022-11-03/"
        },
        {
            "title": "Ransomware Attack on Belarusian Railway (January 2022, Belarus)",
            "description": (
                "A hacktivist group known as the “Cyber Partisans” launched a ransomware attack against the Belarusian Railway. The attack reportedly "
                "encrypted key IT systems, including e-ticketing platforms, causing significant service disruptions. This event highlighted how geopolitical "
                "tensions can manifest as cyber conflicts targeting critical infrastructure."
            ),
            "link_text": "Read more (Reuters)",
            "url": "https://www.reuters.com/world/europe/belarusian-railway-services-disrupted-by-cyber-attack-local-media-2022-01-24/"
        },
        {
            "title": "Radio Signal Hack on PKP Polish State Railways (August 2023, Poland)",
            "description": (
                "Cybercriminals exploited legacy radio technology by broadcasting unauthorized emergency stop commands over the railway’s radio network. "
                "This novel attack resulted in the halting of approximately **20 trains** for a few hours, emphasizing the importance of securing "
                "Operational Technology (OT) and communication channels, including older systems."
            ),
            "link_text": "Read more (WIRED)",
            "url": "https://www.wired.com/story/poland-train-radio-stop-hack/"
        },
         {
            "title": "Website Hack of Dublin’s Luas Tram System (January 2019, Ireland)",
            "description": (
                "The Luas tram system’s website was hacked and defaced with a ransom demand for Bitcoin. While this particular attack did not directly "
                "impact tram operations, it served as an important local reminder of vulnerabilities in public-facing digital assets within Ireland’s transport infrastructure."
            ),
            "link_text": "Read more (TheJournal.ie)",
            "url": "https://www.thejournal.ie/luas-website-hack-bitcoin-4424357-Jan2019/"
        },
    ]

    # Display each incident in an expander for a cleaner UI
    for incident in incidents:
        with st.expander(f"**{incident['title']}**"):
            st.markdown(incident["description"])
            st.markdown(f"[{incident['link_text']}]({incident['url']})") # Link to learn more
    
    st.markdown("---") # Visual separator
    # Concluding message reinforcing collective responsibility
    st.markdown(
        """
        #### Our Collective Responsibility at Iarnród Éireann

        These incidents underscore a clear message: cybersecurity is not solely an IT department concern. Every employee at Iarnród Éireann has a part to play. 
        By understanding common threats like phishing, practicing good password hygiene, being cautious with data, and knowing how to report suspicious activity, 
        we collectively strengthen our defences. 

        This RailSecure Learning Platform is designed to equip you with the knowledge and skills to be that strong first line of defence. 
        Your vigilance helps protect our operations, our data, our colleagues, and the thousands of passengers who rely on us every day. 
        Let's work together to keep Iarnród Éireann secure and resilient in the face of evolving cyber threats.
        """
    )
