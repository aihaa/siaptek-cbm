# from twilio.rest import Client
# import os
# from dotenv import load_dotenv

# def send_sms_via_twilio(to_number, message):
#     try:
#         # Load environment variables from .env file
#         load_dotenv()

#         # Twilio credentials from the Twilio console
#         account_sid = os.getenv('TWILIO_ACCOUNT_SID')
#         auth_token = os.getenv('TWILIO_AUTH_TOKEN')
#         twilio_number = os.getenv('TWILIO_PHONE_NUMBER')

#         # Initialize Twilio client
#         client = Client(account_sid, auth_token)

#         # Send the SMS
#         message = client.messages.create(
#             body=message,
#             from_=twilio_number,
#             to=to_number
#         )

#         print(f"Message sent successfully: {message.sid}")
#     except Exception as e:
#         print(f"Error sending SMS: {e}")







# # import pywhatkit
# # import datetime

# # def sms_notification():
# #     try:
# #         # Current time
# #         now = datetime.datetime.now()

# #         # Sending the message 1 minute from now
# #         time_hour = now.hour
# #         time_min = now.minute + 1

# #         # Make sure the minutes are within 0-59
# #         if time_min >= 60:
# #             time_hour += 1
# #             time_min -= 60

# #         pywhatkit.sendwhatmsg(phone_no="+60129462206", message="ALERT! threshold exceed for engine M45T", time_hour=time_hour, time_min=time_min)
# #     except Exception as e:
# #         print(f"Error in sms notification: {e}")