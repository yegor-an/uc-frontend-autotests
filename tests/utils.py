import random
import string

def generate_email(user_length=6, domain_length=5, tld_list=None):
    if tld_list is None:
        tld_list = ["com", "net", "org", "tech", "io"]

    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=user_length))
    domain = ''.join(random.choices(string.ascii_lowercase, k=domain_length))
    tld = random.choice(tld_list)

    return f"{username}@{domain}.{tld}"