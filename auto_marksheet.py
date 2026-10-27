"""
Auto-Marksheet-Generator
An automated Python pipeline that scrapes academic result portals 
and generates downloadable PDF marksheets instantly.
"""

import requests
from bs4 import BeautifulSoup
import pdfkit
import sys

# ==========================================
# CONFIGURATION - SANITIZED FOR PUBLIC REPO
# ==========================================
LOGIN_URL = "https://erp.iitkgp.ac.in/IIT_ERP3/" # Replace with actual auth URL
RESULTS_URL = "https://erp.iitkgp.ac.in/StudentPerformance/" # Replace with actual data URL

# Judges/Users will input their own credentials here
USERNAME = "YOUR_ROLL_NUMBER_HERE"
PASSWORD = "YOUR_PASSWORD_HERE"
# ==========================================


def login_to_portal(session, username, password):
    """Authenticates the session with the academic portal."""
    print("[*] Attempting to log in...")
    
    login_payload = {
        'user_id': username,
        'password': password,
        # Add any other hidden form fields (like CSRF tokens) your specific Colab script uses
    }
    
    response = session.post(LOGIN_URL, data=login_payload)
    
    if response.status_code == 200 and "Dashboard" in response.text:
        print("[+] Login successful.")
        return True
    else:
        print("[-] Login failed. Check credentials or CAPTCHA requirements.")
        return False


def fetch_and_parse_results(session):
    """Scrapes the HTML marksheet data from the portal."""
    print("[*] Fetching academic results...")
    
    response = session.get(RESULTS_URL)
    soup = BeautifulSoup(response.text, 'lxml')
    
    # Isolate the table or div containing the actual grades
    # Update the target ID/Class based on your exact Colab DOM inspection
    marksheet_html = soup.find('div', {'id': 'marksheet-container'})
    
    if not marksheet_html:
        print("[-] Could not locate marksheet data on the page.")
        sys.exit(1)
        
    return str(marksheet_html)


def generate_pdf(html_content, output_filename="Marksheet.pdf"):
    """Converts the scraped HTML data into a cleanly formatted PDF."""
    print(f"[*] Generating {output_filename}...")
    
    # Wrap the extracted table in basic HTML boilerplate for clean PDF rendering
    full_html = f"""
    <html>
    <head><style>
        body {{ font-family: Arial, sans-serif; padding: 20px; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ border: 1px solid black; padding: 8px; text-align: center; }}
        th {{ background-color: #f2f2f2; }}
    </style></head>
    <body>
        <h2>Academic Performance Report</h2>
        {html_content}
    </body>
    </html>
    """
    
    try:
        # Note: wkhtmltopdf must be installed on the system for pdfkit to work
        pdfkit.from_string(full_html, output_filename)
        print(f"[+] Success! PDF saved as {output_filename}")
    except Exception as e:
        print(f"[-] Error generating PDF: {e}")


def main():
    # Start a persistent requests session to handle cookies automatically
    with requests.Session() as session:
        # Step 1: Log in
        if login_to_portal(session, USERNAME, PASSWORD):
            
            # Step 2: Scrape the data
            raw_html = fetch_and_parse_results(session)
            
            # Step 3: Export to PDF
            generate_pdf(raw_html)

if __name__ == "__main__":
    main()