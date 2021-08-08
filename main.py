import base64
import os

from datastore import DataStore
from emailsender import EmailSender

sendgrid_api_key = os.environ.get('SENDGRID_EMAIL_API_KEY', 'Specified environment variable is not set.')
travel_site_url = os.environ.get('TRAVEL_SITE_URL', 'Specified environment variable is not set.')
sender = os.environ.get('SENDER', 'Specified environment variable is not set.')

datastore_client = DataStore()
email_sender = EmailSender(sendgrid_api_key)

def get_message_content(last_update):
    return ("US Gov Travel restrictions page was recently updated (" + last_update + ").\n" 
            "Go to " + travel_site_url)

def send_email_notification(event, context):

    last_update = base64.b64decode(event['data']).decode('utf-8')

    context = datastore_client.get_context()
    last_updated_saved = context['last_updated_at']

    print('Last saved update date was: ' + last_updated_saved)
    print('Current update date is: ' + last_update)

    if last_update != last_updated_saved:

        print('A new update was pushed. Updating database and notifying subscribers')

        datastore_client.update_context(context, last_update)

        recipients = datastore_client.get_recipients()
        content = get_message_content(last_update)
        subject = 'Travel Ban Cron Job Notification'

        email_sender.send(sender, recipients, subject, content)