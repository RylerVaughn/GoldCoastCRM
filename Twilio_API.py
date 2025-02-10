from twilio.rest import Client
import os

class Twilio_API():        
    def send_message(self, client_number: str, message: str):
        client = Client(
            'AC959f452137bd815efcc433083914b75f',
            os.environ.get('TWILIO_AUTH_TOKEN')
        )
        client.messages.create(
            from_='+18127821348',
            body=message,
            to=client_number
        )
        