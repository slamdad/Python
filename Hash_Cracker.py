#!/usr/bin/env python3
"""
Hash Cracker
Python for Pentesters - Task 6

Performs a dictionary attack against a target hash by computing
the hash of each wordlist candidate and comparing it to the target.
Supports MD5, SHA-1, SHA-256, SHA-512, and other hashlib algorithms.

Usage:
    python3 hash_cracker.py <hash> <wordlist> [algorithm]

Examples:
    python3 hash_cracker.py 5f4dcc3b5aa765d61d8327deb882cf99 wordlist.txt md5
    python3 hash_cracker.py a1b2c3d4... wordlist.txt sha256
"""

import hashlib  # Provides the hashing algorithms (MD5, SHA256, etc.)
import sys      # Used to read command-line arguments and exit cleanly


def compute_hash(text, algorithm="md5"):
    """Compute the hash of a string using the specified algorithm."""
    # hashlib.new() lets us pick the algorithm dynamically at runtime
    h = hashlib.new(algorithm)
    # Hashers require bytes, so we encode the string into UTF-8 bytes
    h.update(text.encode())
    # hexdigest() returns the final hash as a readable hex string
    return h.hexdigest()


def crack_hash(target_hash, wordlist_path, algorithm="md5"):
    """Attempt to find the plaintext for a hash using a wordlist."""
    try:
        # 'with' ensures the file closes automatically, even if we crash
        with open(wordlist_path, "r") as f:
            # Looping directly over the file object is memory-efficient
            # (reads line-by-line instead of loading everything into RAM)
            for line_number, line in enumerate(f, start=1):
                # Remove trailing newlines/spaces from the wordlist entry
                candidate = line.strip()
                
                # Skip blank lines to avoid hashing empty strings
                if not candidate:
                    continue

                # Hash the current candidate word
                candidate_hash = compute_hash(candidate, algorithm)
                print(f"[*] {candidate} -> {candidate_hash}")  # show work

                # .lower() ensures uppercase target hashes still match
                if candidate_hash == target_hash.lower():
                    print(f"[+] Match found after {line_number} attempts!")
                    print(f"[+] Plaintext: {candidate}")
                    return candidate  # Stop searching once we find it

        # Reached only if the loop completes without returning
        print(f"[-] Exhausted wordlist. No match found.")
        return None

    # Gracefully handle a bad file path instead of crashing
    except FileNotFoundError:
        print(f"[!] Wordlist not found: {wordlist_path}")
        return None


def main():
    # sys.argv[0] is the script name, so we need at least 3 items total
    if len(sys.argv) < 3:
        print(f"Usage: python3 {sys.argv[0]} <hash> <wordlist> [algorithm]")
        print(f"Example: python3 {sys.argv[0]} 5f4dcc3b5aa765d61d8327deb882cf99 wordlist.txt md5")
        print(f"Supported: md5, sha1, sha256, sha512")
        sys.exit(1)  # Exit with code 1 to signal an error

    # Parse command-line arguments into variables
    target_hash = sys.argv[1]
    wordlist_path = sys.argv[2]
    # If a third argument exists, use it; otherwise default to "md5"
    algorithm = sys.argv[3] if len(sys.argv) > 3 else "md5"

    # Print the configuration so the user knows what's happening
    print(f"[*] Target hash: {target_hash}")
    print(f"[*] Algorithm:   {algorithm}")
    print(f"[*] Wordlist:    {wordlist_path}")
    print(f"[*] Cracking...\n")

    # Call the cracking function
    result = crack_hash(target_hash, wordlist_path, algorithm)

    # Print a final summary based on whether a match was found
    if result:
        print(f"\n[*] Hash cracked successfully.")
    else:
        print(f"\n[*] Try a larger wordlist or a different algorithm.")


# Standard Python idiom: only run main() if executed as a script,
# not if imported as a module into another script.
if __name__ == "__main__":
    main()