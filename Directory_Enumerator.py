#!/usr/bin/env python3
"""
Directory Enumeration Tool
Reads directory/file name candidates from a wordlist and tests each one
against a target URL by appending the candidate and a file extension.
"""

import requests  # For making HTTP requests
import sys       # For command-line arguments

def load_wordlist(filepath):
    """Read a wordlist file and return a list of stripped lines."""
    try:
        # Open the file and read it line-by-line
        with open(filepath, "r") as f:
            # Strip newlines and ignore blank lines using a list comprehension
            words = [line.strip() for line in f if line.strip()]
        print(f"[*] Loaded {len(words)} entries from {filepath}")
        return words
    except FileNotFoundError:
        # Gracefully handle a missing wordlist
        print(f"[!] Error: '{filepath}' not found.")
        return []

def enumerate_directories(target_url, wordlist, extension=".html"):
    """Test each directory/file candidate against the target URL."""
    found = []

    # Loop through every word in the wordlist
    for entry in wordlist:
        # Build the full URL (e.g., http://target.com/admin.html)
        url = f"{target_url}/{entry}{extension}"
        
        try:
            # Request the URL; wait a maximum of 3 seconds before timing out
            r = requests.get(url, timeout=3)
            
            # If the server responds with anything other than 404 Not Found
            # (e.g., 200 OK, 301 Redirect, 403 Forbidden), the path exists
            if r.status_code != 404:
                print(f"[+] {r.status_code} - {url}")
                found.append(url)
                
        # Ignore connection errors and timeouts so one dead link doesn't stop the scan
        except requests.ConnectionError:
            pass
        except requests.Timeout:
            pass

    return found

def main():
    # Ensure the user provided at least the URL and the wordlist
    if len(sys.argv) < 3:
        print(f"Usage: python3 {sys.argv[0]} <target_url> <wordlist> [extension]")
        print(f"Example: python3 {sys.argv[0]} http://10.10.10.5 wordlist.txt .html")
        sys.exit(1)

    # Parse command-line arguments
    target_url = sys.argv[1]
    wordlist_path = sys.argv[2]
    # Use a third argument if provided, otherwise default to ".html"
    extension = sys.argv[3] if len(sys.argv) > 3 else ".html"

    print(f"[*] Starting directory enumeration for {target_url}")
    wordlist = load_wordlist(wordlist_path)

    # Exit if the wordlist is empty or failed to load
    if not wordlist:
        print("[!] No words to test. Exiting.")
        sys.exit(1)

    # Run the enumeration and print the final count
    results = enumerate_directories(target_url, wordlist, extension)
    print(f"\n[*] Enumeration complete. Found {len(results)} valid path(s).")

# Run the main function if executed directly
main()