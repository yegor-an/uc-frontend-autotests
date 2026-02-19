import random
import string

def generate_email(user_length=6, domain_length=5):
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=user_length))
    domain = "autogen"
    tld = "ye"

    return f"{username}@{domain}.{tld}"
    

def save_email(filename, email):
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"\n{email}")


def get_last_email(filename):
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()
    return lines[-1].strip() if lines else None


def remove_email(filename, email):
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()
    with open(filename, "w", encoding="utf-8") as f:
        for line in lines:
            if line.strip() != email:
                f.write(line)
