import os
import slackapi
import db

WEBHOOK_URL = os.environ.get('WEBHOOK_URL')

for goal in db.fetch_goals():
    slackapi.post_direct_message(goal['user_id'], text=goal['content'])
