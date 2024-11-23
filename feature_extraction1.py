# Import required libraries
import streamlit as st
import whois
import requests
from urllib.parse import urlparse
import re
import datetime
from sklearn.ensemble import RandomForestClassifier

# Feature extraction function
def extract_features_from_url(url):
    try:
        features = []
        
        # 1. having_IP_Address
        ip_pattern = re.compile(r'(\d{1,3}\.){3}\d{1,3}')
        features.append(-1 if ip_pattern.search(url) else 1)
        
        # 2. URL_Length
        features.append(-1 if len(url) > 54 else 1)
        
        # 3. Shortening_Service
        shortening_services = ["bit.ly", "tinyurl", "goo.gl", "t.co", "ow.ly"]
        features.append(-1 if any(service in url for service in shortening_services) else 1)
        
        # 4. having_At_Symbol
        features.append(-1 if "@" in url else 1)
        
        # 5. double_slash_redirecting
        features.append(-1 if url.startswith("//") else 1)
        
        # 6. Prefix_Suffix
        features.append(-1 if "-" in urlparse(url).netloc else 1)
        
        # 7. having_Sub_Domain
        domain_parts = urlparse(url).netloc.split(".")
        features.append(-1 if len(domain_parts) > 3 else 1)
        
        # 8. SSLfinal_State
        try:
            response = requests.get(url, timeout=5)
            features.append(1 if response.url.startswith("https") else -1)
        except:
            features.append(-1)
        
        # 9. Domain_registeration_length
        try:
            domain_info = whois.whois(urlparse(url).netloc)
            if domain_info and domain_info.expiration_date:
                expiration_date = domain_info.expiration_date
                if isinstance(expiration_date, list):
                    expiration_date = expiration_date[0]
                registration_length = (expiration_date - datetime.datetime.now()).days
                features.append(1 if registration_length > 365 else -1)
            else:
                features.append(-1)
        except:
            features.append(-1)
        
        # 10. Favicon (placeholder, assume safe)
        features.append(1)
        
        # 11. port (placeholder, assume safe)
        features.append(1)
        
        # 12. HTTPS_token
        features.append(-1 if "https-" in urlparse(url).netloc else 1)
        
        # Add placeholders for remaining features
        features.extend([1] * (30 - len(features)))  # Ensure 30 features
        
        return features
    except Exception as e:
        st.error(f"Error extracting features: {e}")
        return [0] * 30  # Return default to avoid crashes
