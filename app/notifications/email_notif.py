import os
import smtplib
import getpass
from pathlib import Path

from dotenv import load_dotenv

def email_notification(to_email, data_point, threshold):
    try:
        HOST = "smtp-mail.outlook.com"
        PORT = 587

        # Load enviroment variables
        # current_dir = Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd()
        # envars = current_dir / ".env"
        # load_dotenv(envars)
        load_dotenv()

        # Read environment variables
        TO_EMAIL = to_email
        FROM_EMAIL = os.getenv("EMAIL")
        PASSWORD_EMAIL = os.getenv("PASSWORD")

        # FROM_EMAIL = "aimanfatihahh@hotmail.com"
        # TO_EMAIL = "aimanfatihahahmadrazif@gmail.com"
        # FROM_EMAIL = from_email
        # TO_EMAIL = to_email
        # PASSWORD = getpass.getpass("Enter password: ")



        MESSAGE = f"""Subject: ALERT!

        Hi Mr. Arif, This email is notifying data point {data_point} is exceeding threshold {threshold} on engine M45R.
        """

        # msg = MIMEText(BODY)
        # msg['Subject'] = "ALERT!"
        # msg['From'] = FROM_EMAIL
        # msg['To'] = TO_EMAIL
        # msg['Cc'] = "17206983@siswa.um.edu.my"

        # html = ""
        # with open("mail.html", "r") as file:
        #     html = file.read()

        # html_part = MIMEText(html, 'html')
        # msg.attach(html_part)

        smtp = smtplib.SMTP(HOST, PORT)

        status_code, response = smtp.ehlo()
        print(f"[*] Echoing the server: {status_code} {response}")

        status_code, response = smtp.starttls()
        print(f"[*] Starting TLS connection: {status_code} {response}")

        status_code, response = smtp.login(FROM_EMAIL, PASSWORD_EMAIL)
        print(f"[*] Logging in: {status_code} {response}")

        smtp.sendmail(FROM_EMAIL, TO_EMAIL, MESSAGE)
        smtp.quit()
    except Exception as e:
        print(f"Error in email notification: {e}")