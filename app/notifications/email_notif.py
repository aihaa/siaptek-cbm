import smtplib
import getpass

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

HOST = "smtp-mail.outlook.com"
PORT = 587

FROM_EMAIL = "aimanfatihahh@hotmail.com"
TO_EMAIL = "aimanfatihahahmadrazif@gmail.com"
PASSWORD = getpass.getpass("Enter password: ")

MESSAGE = """Subject: ALERT!
Hi Mr. Arif,

This email is notifying an exceeding threshold on engine M45R.
"""

# msg = MIMEMultipart("alternative")
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

status_code, response = smtp.login(FROM_EMAIL, PASSWORD)
print(f"[*] Logging in: {status_code} {response}")

smtp.sendmail(FROM_EMAIL, TO_EMAIL, MESSAGE)
smtp.quit()
