import os

from twilio.rest import Client


class Messaging:
    def __init__(self):
        self.account_sid = 'AC513b80084d28011323c6b55ae90a0cae'
        self.auth_token = 'a6a57ca78f3c141aeb56469094ffbfde'
        self.client = Client(self.account_sid, self.auth_token)
        self.tw_number = '+12512209502'

    def send(self, body, to):
        message = self.client.messages.create(
            body=body,
            from_=self.tw_number,
            to=to
        )
        return message.sid
