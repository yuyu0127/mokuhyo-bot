import os

import blockkit
import db
import slackapi

__import__('dotenv').load_dotenv()
WEBHOOK_URL = os.environ.get('WEBHOOK_URL')


def check(goal):
    user_id = goal['user_id']
    content = goal['content']
    blocks = [
        blockkit.section(
            f'今日の目標 `{content}` は達成できたかな？\n（今できていなくても、すぐにできそうであれば、実行して「できた！✋」を押そう）'),
        blockkit.actions([
            blockkit.button('できた！✋', 'completed', 'True', style='primary'),
            blockkit.button('できなかった…', 'completed', 'False'),
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
