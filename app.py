from flask import Flask, jsonify, request, Response
import json
import blockkit
import os
import slackapi

app = Flask(__name__)


WEBHOOK_URL = os.environ.get('WEBHOOK_URL')


@app.route('/command', methods=['POST'])
def handle_command():
    print(request.form.to_dict())
    workspace_name: str = request.form.get('team_domain')
    user: str = request.form.get('user_id')
    type: str = request.form.get('command')
    text: str = request.form.get('text')

    if type == '/mokuhyo':
        blocks = [
            blockkit.section(f'今日の目標は `{text}` だね！\nみんなに宣言する？'),
            blockkit.actions([
                blockkit.button('する！✋', 'declare', 'True', style='primary'),
                blockkit.button('しない', 'declare', 'False', style='primary'),
            ])
        ]
        json_dict = {
            'response_type': 'ephemeral',
            'blocks': blocks
        }
        return jsonify(json_dict), 200
    return '', 200


@app.route('/interactive', methods=['POST'])
def handle_interactive():
    print(request.form.to_dict())

    payload = json.loads(request.form.to_dict()['payload'])
    print(payload)
    url = payload['response_url']
    slackapi.post_message(url, text=payload, response_type='ephemeral')
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
