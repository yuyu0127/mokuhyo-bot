import os
import slackapi
import db

__import__('dotenv').load_dotenv()
WEBHOOK_URL = os.environ.get('WEBHOOK_URL')

for goal in db.fetch_goals():
    print(goal)
    try:
        res = slackapi.post_direct_message(
            goal['user_id'], text=goal['content'])
        print(res.json())
    except Exception as e:
        print(e)
