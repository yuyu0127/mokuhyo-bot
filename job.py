import os

import blockkit
import db
import slackapi
from localization import l8n

__import__('dotenv').load_dotenv()
WEBHOOK_URL = os.environ.get('WEBHOOK_URL')


def check(goal):
    '''
    達成できたかの確認をDMで送る
    '''
    user_id = goal['user_id']
    content = goal['content']

    # DM送信
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

    # DBにチェックしたフラグを設定
    db.set_checked(user_id, True)

    return res


def main():
    print('[Checking if Completed]')
    for goal in db.fetch_goals():
        print(goal)
        try:
            if goal['checked'] == False:
                check(goal)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    main()
