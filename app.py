from flask import Flask, jsonify, request, Response
import json
import blockkit
import db
import os
import slackapi
from datetime import datetime
app = Flask(__name__)


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
    resp_url = payload['response_url']
    action = payload['actions'][0]
    act_value = action['value']
    act_id = action['action_id']
    user_id = payload['user']['id']

    if act_value == 'declare' and act_id == 'True':
        goal = db.fetch_goal(user_id)
        text = f'<@{user_id}> さんが、今日の目標📝 を宣言しました！\n```{goal["content"]}```'
        slackapi.post_message(WEBHOOK_URL, text=text)
    if act_value == 'completed' and act_id == 'True':
        text = f'<@{user_id}> さんが、目標 `{goal["content"]}` を達成したようです😊'
        slackapi.post_message(WEBHOOK_URL, text=text)

    return '', 200


def check():
    blocks = [
        blockkit.section('今日の目標は達成できたかな？'),
        blockkit.actions([
            blockkit.button('できた！✋', 'completed', 'True', style='primary'),
            blockkit.button('できなかった…', 'completed', 'False'),
        ])
    ]

    json_dict = {
        'response_type': 'ephemeral',
        'blocks': blocks
    }


if __name__ == '__main__':
    app.run()
