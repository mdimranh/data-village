import requests


class Messaging:
    def __init__(self):
        self.url = "http://bulksmsbd.net/api/smsapi?api_key=3ufEeIKgOxKBURN0kdok&type=text&senderid=8809617618371"

    def send(self, body, to):
        url = self.url + f"&number={to}" + f"&message={body}"
        requests.get(url)
