import time
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import os

# === CONFIG ===
URL = "https://www.videohry.tv/kategoria/sega/"
CHECK_INTERVAL = 300  # in seconds

# Use environment variables for security
EMAIL_SENDER = os.environ["EMAIL_SENDER"]
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]
EMAIL_RECEIVER = os.environ["EMAIL_RECEIVER"]

last_content = ""

def get_website_content():
    try:
        response = requests.get(URL, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.get_text().strip()
    except Exception as e:
        print("Error fetching website:", e)
        return ""

def send_email(subject, body):
    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER

        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("Email sent.")
    except Exception as e:
        print("Error sending email:", e)

def main():
    global last_content
    print("Monitoring started...")

    while True:
        current_content = get_website_content()
        if current_content and current_content != last_content:
            if last_content != "":
                print("Change detected, sending email...")
                send_email("Nieco sa tu veru zmenilo!", f"Tu to checkni {URL}")
            last_content = current_content
        else:
            print("No changes.")

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
