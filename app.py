from flask import Flask, jsonify, request, Response
import json
import blockkit
import db
import os
import slackapi
from datetime import datetime
app = Flask(__name__)

__import__('dotenv').load_dotenv()
WEBHOOK_URL = os.environ.get('WEBHOOK_URL')


@app.route('/command', methods=['POST'])
def handle_command():
    payload = request.form.to_dict()
    print(payload)
    workspace_name: str = payload['team_domain']
    user_id: str = payload['user_id']
    type: str = payload['command']
    text: str = payload['text']

    if type == '/mokuhyo':
        db.register_goal(datetime.now(), user_id, text)
        blocks = [
            blockkit.section(f'今日の目標は `{text}` だね！\nみんなに宣言する？'),
            blockkit.actions([
                blockkit.button('する！✋', 'declare', 'True', style='primary'),
                blockkit.button('しない', 'declare', 'False'),
            ])
        ]
        json_dict = {
            'response_type': 'ephemeral',
            'replace_original': True,
            'blocks': blocks
        }
        return jsonify(json_dict), 200
    return '', 200


@app.route('/interactive', methods=['POST'])
def handle_interactive():
    payload = json.loads(request.form.to_dict()['payload'])
    print('Interactive Payload', payload)
    resp_url = payload['response_url']
    action = payload['actions'][0]
    act_value = action['value']
    act_id = action['action_id']
    user_id = payload['user']['id']

    channel_id = payload['container']['channel_id']
    message_ts = payload['container']['message_ts']
    res = slackapi.delete_message(channel_id, message_ts)
    print(res.json())

    if act_value == 'declare' and act_id == 'True':
        goal = db.fetch_goal(user_id)
        text = f'<@{user_id}> さんが、目標 `{goal["content"]}` を宣言しました！📝'
        slackapi.webhook_message(WEBHOOK_URL, text=text)
    if act_value == 'completed':
        if act_id == 'True':
            db.set_completed(user_id, True)
            goal = db.fetch_goal(user_id)
            text = f'<@{user_id}> さんが、目標 `{goal["content"]}` を達成したようです😊'
            slackapi.webhook_message(WEBHOOK_URL, text=text)
            return '達成おめでとう！', 200
        else:
            db.set_completed(user_id, False)
            return '次また頑張ろう！', 200

    return '', 200


if __name__ == '__main__':
    app.run()
