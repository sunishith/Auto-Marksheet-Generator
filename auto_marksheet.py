"""
Auto-Marksheet-Generator (Mock Data Version)
An automated Python pipeline that scrapes academic result portals 
and generates downloadable PDF marksheets instantly.
"""

import requests
import pdfkit

def fetch_and_parse_results(session):
    """Simulates the HTML data since the live portal is currently closed."""
    print("[*] Academic portal is currently offline.")
    print("[*] Bypassing network request. Injecting mock HTML data for demonstration...")
    
    mock_html_data = """
    <div id="marksheet-container">
        <table border="1">
            <tr><th>Subject ID</th><th>Subject Name</th><th>Grade</th></tr>
            <tr><td>CS10001</td><td>Programming and Data Structures</td><td>A</td></tr>
            <tr><td>PH11001</td><td>Physics</td><td>A</td></tr>
            <tr><td>ME10001</td><td>Mechanics</td><td>EX</td></tr>
        </table>
    </div>
    """
    return mock_html_data


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
    # Start a persistent requests session
    with requests.Session() as session:
        # Step 1: Simulate Login
        print("[+] Mock login successful.")
        
        # Step 2: Load the mock data instead of scraping
        raw_html = fetch_and_parse_results(session)
        
        # Step 3: Export to PDF
        generate_pdf(raw_html)


if __name__ == "__main__":
    main()
