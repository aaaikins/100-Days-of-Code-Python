import os
from twilio.rest import Client


class NotificationManager:
    def __init__(self):
        """
        Initialize the NotificationManager class.
        Sets up the Twilio client using credentials from environment variables.
        """
        # Initialize the Twilio client with SID and Auth Token from environment variables
        self.client = Client(os.environ['TWILIO_SID'], os.environ["TWILIO_AUTH_TOKEN"])

    def send_whatsapp(self, message_body):
        """
        Send a WhatsApp message using Twilio.
        """
        # Send the message using the Twilio client
        message = self.client.messages.create(
            from_=f'whatsapp:{os.environ["TWILIO_WHATSAPP_NUMBER"]}',  # Sender's WhatsApp number
            body=message_body,  # The message content
            to=f'whatsapp:{os.environ["TWILIO_VERIFIED_NUMBER"]}'  # Recipient's WhatsApp number
        )
        # Print the message SID (unique identifier for the message)
        print(message.sid)
