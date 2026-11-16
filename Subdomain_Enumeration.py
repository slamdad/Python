#!/usr/bin/env python3
"""
Subdomain Enumeration Tool
Reads potential subdomain names from a wordlist, prepends each one
to a target domain, and tests for valid responses via HTTP.
"""

import requests  # For making HTTP requests and catching DNS errors
import sys       # For command-line arguments

def load_wordlist(filepath):
    """Read a wordlist file and return a list of stripped lines."""
    try:
        # Open the file and read line-by-line, skipping blanks
        with open(filepath, "r") as f:
            words = [line.strip() for line in f if line.strip()]
        print(f"[*] Loaded {len(words)} entries from {filepath}")
        return words
    except FileNotFoundError:
        print(f"[!] Error: '{filepath}' not found.")
        return []

def enumerate_subdomains(domain, wordlist):
    """Test each subdomain candidate against the target domain."""
    found = []

    # Iterate through each subdomain word (e.g., "dev", "mail", "admin")
    for sub in wordlist:
        # Construct the full URL
        url = f"http://{sub}.{domain}"
        
        try:
            # Send a GET request. If the subdomain doesn't exist in DNS,
            # requests will raise a ConnectionError (caught below).
            requests.get(url, timeout=3)
            print(f"[+] Found: {url}")
            found.append(url)
            
        # Ignore dead subdomains and timeouts
        except requests.ConnectionError:
            pass
        except requests.Timeout:
            pass

    return found

def main():
    # Ensure the user provided exactly two arguments (domain and wordlist)
    if len(sys.argv) != 3:
        print(f"Usage: python3 {sys.argv[0]} <domain> <wordlist>")
        print(f"Example: python3 {sys.argv[0]} example.com subdomains.txt")
        sys.exit(1)

    # Parse command-line arguments
    domain = sys.argv[1]
    wordlist_path = sys.argv[2]

    print(f"[*] Starting subdomain enumeration for {domain}")
    wordlist = load_wordlist(wordlist_path)

    # Exit if the wordlist is empty
    if not wordlist:
        print("[!] No words to test. Exiting.")
        sys.exit(1)

    # Run enumeration and print total count
    results = enumerate_subdomains(domain, wordlist)
    print(f"\n[*] Enumeration complete. Found {len(results)} subdomain(s).")

# Entry point
main()