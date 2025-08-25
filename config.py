import os

if not os.getenv("GITHUB_ACTIONS"):  
    from dotenv import load_dotenv
    load_dotenv()

BASE_URL = os.getenv("BASE_URL")
EMAIL = os.getenv("TEST_EMAIL_1")
PASSWORD = os.getenv("TEST_PASSWORD")
USERNAME = os.getenv("TEST_USERNAME") 

