from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

class EmailSender:

    def __init__(self, api_key):
        self.__client = SendGridAPIClient(api_key)

    def send(self, sender, recipients, subject, content):

        message = Mail(
            from_email=sender,
            to_emails=recipients,
            subject=subject,
            html_content=content)

        try:
            self.__client.send(message)
        except Exception as e:
            print(e)