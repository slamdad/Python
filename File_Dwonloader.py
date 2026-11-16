#!/usr/bin/env python3
"""
File Downloader
Downloads files from URLs with error handling. Supports single-file
downloads, batch downloads from a URL list file, and streaming for large files.
"""

import requests  # For making HTTP requests
import sys       # For command-line arguments
import os        # For file path operations and directory creation

def download_file(url, output_path):
    """Download a file from a URL and save it locally."""
    try:
        # Fetch the file, following redirects, with a 10-second timeout
        r = requests.get(url, allow_redirects=True, timeout=10)
        
        # Raise an exception for 4xx/5xx status codes (e.g., 404 Not Found)
        r.raise_for_status()

        # Write the raw bytes to disk (wb = write binary)
        with open(output_path, "wb") as f:
            f.write(r.content)

        print(f"[+] Downloaded: {output_path} ({len(r.content)} bytes)")
        return True

    # Catch specific network errors to prevent the script from crashing
    except requests.ConnectionError:
        print(f"[!] Connection failed: {url}")
        return False
    except requests.Timeout:
        print(f"[!] Request timed out: {url}")
        return False
    except requests.HTTPError as e:
        print(f"[!] HTTP error: {e}")
        return False


def download_large_file(url, output_path, chunk_size=8192):
    """Download a file using streaming to handle large files efficiently."""
    try:
        # stream=True tells requests not to load the whole file into memory
        r = requests.get(url, stream=True, allow_redirects=True, timeout=30)
        r.raise_for_status()

        total = 0
        with open(output_path, "wb") as f:
            # Read the file in 8KB chunks and write them to disk one by one
            for chunk in r.iter_content(chunk_size=chunk_size):
                f.write(chunk)
                total += len(chunk)

        print(f"[+] Downloaded: {output_path} ({total} bytes)")
        return True

    # Catch all network/HTTP errors in a single tuple
    except (requests.ConnectionError, requests.Timeout, requests.HTTPError) as e:
        print(f"[!] Download failed: {e}")
        return False


def download_from_list(url_list, output_dir="downloads"):
    """Download files from a list of URLs into the specified directory."""
    # Create the output directory; ignore error if it already exists
    os.makedirs(output_dir, exist_ok=True)
    results = {"success": 0, "failed": 0}

    for url in url_list:
        # Extract filename from the URL (e.g., "http://a.com/b.zip" -> "b.zip")
        filename = url.split("/")[-1]
        
        # Fallback for URLs that end in a slash (like a homepage)
        if not filename:
            filename = "index.html"
            
        # Combine the output directory and filename safely
        output_path = os.path.join(output_dir, filename)

        if download_file(url, output_path):
            results["success"] += 1
        else:
            results["failed"] += 1

    print(f"\n[*] Complete: {results['success']} downloaded, {results['failed']} failed")
    return results


def main():
    # Ensure the user provided at least one argument
    if len(sys.argv) < 2:
        print(f"Usage: python3 {sys.argv[0]} <url_or_file>")
        sys.exit(1)

    target = sys.argv[1]

    # Check if the argument is a local file (e.g., urls.txt)
    if os.path.isfile(target):
        with open(target, "r") as f:
            # Read all non-empty lines into a list of URLs
            urls = [line.strip() for line in f if line.strip()]
            
        print(f"[*] Loaded {len(urls)} URL(s) from {target}")
        download_from_list(urls)
        
    # Otherwise, treat the argument as a direct URL
    else:
        # Extract filename from URL, or use a default if none exists
        filename = target.split("/")[-1] or "downloaded_file"
        download_file(target, filename)

# Entry point
main()