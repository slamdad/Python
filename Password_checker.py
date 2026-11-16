import string  # Built-in module for checking character types (uppercase, digits, punctuation)

def load_common_passwords(filepath):
    """Load a list of common passwords from a text file."""
    common = []
    try:
        with open(filepath, "r") as f:
            # Read line-by-line, strip whitespace, and lowercase for matching
            for line in f:
                common.append(line.strip().lower())
    except FileNotFoundError:
        # Gracefully handle a missing wordlist without crashing
        print(f"Warning: '{filepath}' not found. Skipping common-password check.")
    return common

def check_password(password, common_list):
    """Evaluate a password and return (score, feedback_list)."""
    score = 0
    feedback = []

    # Length checks: 1 point for >= 8 chars, 1 point for >= 12 chars
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Password should be at least 8 characters.")

    if len(password) >= 12:
        score += 1

    # Character variety checks: add 1 point for each category present
    if any(c in string.ascii_uppercase for c in password):
        score += 1
    else:
        feedback.append("Add at least one uppercase letter.")

    if any(c in string.digits for c in password):
        score += 1
    else:
        feedback.append("Add at least one digit.")

    if any(c in string.punctuation for c in password):
        score += 1
    else:
        feedback.append("Add at least one special character (e.g., !, @, #).")

    # Hard override: If it's a known common password, force score to 0
    if password.lower() in common_list:
        score = 0
        feedback = ["This password is in the common-passwords list. Choose another."]

    return score, feedback

def main():
    # Map the numerical score (0-5) to a strength label
    strength_labels = {
        0: "Weak", 1: "Weak",
        2: "Moderate", 3: "Moderate",
        4: "Strong", 5: "Strong"
    }

    # Load the wordlist into memory once at startup
    common_list = load_common_passwords("common_passwords.txt")

    # Main interactive loop
    while True:
        password = input("\nEnter a password to check (or 'quit' to exit): ")

        if password.lower() == "quit":
            print("Goodbye.")
            break

        if len(password) == 0:
            print("Password cannot be empty. Try again.")
            continue

        # Evaluate the password and get the score + tips
        score, feedback = check_password(password, common_list)
        
        # Look up the text label, defaulting to "Unknown" if score is somehow out of range
        label = strength_labels.get(score, "Unknown")

        print(f"\nStrength: {label} ({score}/5)")

        # Print suggestions for improvement, if any
        if feedback:
            print("Suggestions:")
            for tip in feedback:
                print(f"  - {tip}")

        # Log the result to a file, masking the actual password with asterisks
        with open("password_log.txt", "a") as log:
            log.write(f"Password: {'*' * len(password)} | Strength: {label} ({score}/5)\n")

# Run the program
main()