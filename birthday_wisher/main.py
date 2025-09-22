import datetime as dt
import pandas as pd
import random
import smtplib
import os
import time
from email.message import EmailMessage
from twilio.rest import Client

MY_EMAIL = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASS")
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH = os.getenv("TWILIO_AUTH")
TWILIO_NUMBER = os.getenv("TWILIO_NUMBER", "whatsapp:+14155238886")

BIRTHDAYS_CSV_PATH = "birthday_wisher/birthdays.csv"
TEMPLATE_PATH = "birthday_wisher/letter_templates"

MAX_RETRIES = 3
RETRY_DELAY = 5

def load_birthdays(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Birthday file not found: {file_path}")
    return pd.read_csv(file_path)

def get_templates(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Template folder not found: {path}")
    templates = [f for f in os.listdir(path) if f.startswith("letter_") and f.endswith(".txt")]
    if not templates:
        raise FileNotFoundError("No letter templates found")
    return templates

def send_email(to_address, subject, body):
    if not MY_EMAIL or not EMAIL_PASSWORD:
        raise ValueError("Email credentials not set")
    msg = EmailMessage()
    msg["From"] = MY_EMAIL
    msg["To"] = to_address
    msg["Subject"] = subject
    msg.set_content(body)
    with smtplib.SMTP("smtp.gmail.com", 587, timeout=20) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=EMAIL_PASSWORD)
        connection.send_message(msg)

def send_whatsapp(to_number, message):
    if not TWILIO_SID or not TWILIO_AUTH:
        raise ValueError("Twilio credentials not set")
    client = Client(TWILIO_SID, TWILIO_AUTH)
    if not str(to_number).startswith("whatsapp:"):
        to_number = f"whatsapp:{to_number}"
    client.messages.create(body=message, from_=TWILIO_NUMBER, to=to_number)

def attempt(fn, *args, **kwargs):
    last_exc = None
    for i in range(MAX_RETRIES):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            last_exc = e
            print(f"Attempt {i+1}/{MAX_RETRIES} failed: {e}")
            time.sleep(RETRY_DELAY)
    raise last_exc

def main():
    today = dt.datetime.now()
    data = load_birthdays(BIRTHDAYS_CSV_PATH)
    for c in ["month", "day"]:
        if c not in data.columns:
            raise KeyError(f"CSV must contain '{c}' column")
        data[c] = data[c].astype(int)
    birthdays_today = data[(data["month"] == today.month) & (data["day"] == today.day)]
    if birthdays_today.empty:
        print("No birthdays today.")
        return
    templates = get_templates(TEMPLATE_PATH)
    for _, person in birthdays_today.iterrows():
        template_file = os.path.join(TEMPLATE_PATH, random.choice(templates))
        with open(template_file, "r", encoding="utf-8") as f:
            contents = f.read()
        personalized = contents.replace("[NAME]", str(person.get("name", "")))
        if pd.notna(person.get("email")) and person.get("email"):
            try:
                attempt(send_email, person["email"], "Happy Birthday!", personalized)
                print(f"✅ Email sent to {person['name']} ({person['email']})")
            except Exception as e:
                print(f"❌ Failed to send email to {person['name']}: {e}")
        if pd.notna(person.get("phone")) and person.get("phone"):
            try:
                phone = str(person["phone"]).strip()
                attempt(send_whatsapp, phone, personalized)
                print(f"✅ WhatsApp sent to {person['name']} ({person['phone']})")
            except Exception as e:
                print(f"❌ Failed to send WhatsApp to {person['name']}: {e}")
        if (not person.get("email")) and (not person.get("phone")):
            print(f"⚠️ Skipped {person['name']} (no email or phone)")

if __name__ == "__main__":
    main()
