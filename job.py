import os

import blockkit
import db
import slackapi
from localization import l8n

__import__('dotenv').load_dotenv()
WEBHOOK_URL = os.environ.get('WEBHOOK_URL')


def check(goal):
    user_id = goal['user_id']
    content = goal['content']
    blocks = [
        blockkit.section(
            l8n['confirmDone'].format(content=content)),
        blockkit.actions([
            blockkit.button(l8n['doneButton'], 'completed',
                            'True', style='primary'),
            blockkit.button(l8n['notDoneButton'], 'completed', 'False'),
        ])
    ]
    res = slackapi.post_direct_message(user_id, blocks=blocks)
    return res


for goal in db.fetch_goals():
    print(goal)
    try:
        if goal['completed'] == None:
            check(goal)
    except Exception as e:
        print(e)
