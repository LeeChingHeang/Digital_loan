import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Telegram Bot Configuration
TOKEN = os.getenv("TOKEN")

# Database Configuration
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "loan_service")
DB_CHARSET = "utf8mb4"

# File System Configuration
UPLOAD_DIR = os.environ.get("UPLOAD_DIR", r"C:\lending_system\upload")
TESSERACT_PATH = os.environ.get("TESSERACT_PATH", r"C:\Program Files\Tesseract-OCR\tesseract.exe")

# Rate Limiting Configuration
MAX_ATTEMPTS = 5
TIME_WINDOW = 300  # 5 minutes in seconds

# Conversation States
SELECT_LANGUAGE = 0
AUTHENTICATE = 1
SELECT_TENOR = 2
SELECT_AMOUNT = 3
UPLOAD_DOC = 4
UPLOAD_ID = 5
ID_CONFIRMATION = 100
UPLOAD_SELFIE = 6
USER_INFO = 7
LOAN_ELIGIBILITY = 8
REVIEW = 9
AGREEMENT = 10
CONTRACT = 11
SIGNATURE = 12
SELECT_PAYMENT_SCHEDULE = 13
REPAYMENT_INFO = 14
REPORT = 15
SUPPORT = 16

SIMULATE_AMOUNT = 17
SIMULATE_INTEREST = 18
SIMULATE_TERM = 19

PREAPPROVAL_INPUT = 50
SET_NATIONAL_ID_INPUT = 60
PIN_INPUT = 71
PIN_CONFIRM = 72
PIN_CURRENT = 74
PREAPPROVAL_AUTH = 75

NEW_USER_CHOICE = 1000
PREAPPROVAL_CHOICE = 1001
PREAPPROVAL_USER_INFO = 1002