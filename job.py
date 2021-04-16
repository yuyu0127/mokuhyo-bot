import os
import slackapi

WEBHOOK_URL = os.environ.get('WEBHOOK_URL')

slackapi.post_message(WEBHOOK_URL, text="TEST")
