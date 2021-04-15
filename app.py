from flask import Flask, jsonify, request, Response

import json
import blockkit
import slackapi

app = Flask(__name__)


@app.route('/command', methods=["POST"])
def handle_command():
    print(request.form.to_dict())
    workspace_name: str = request.form.get('team_domain')
    user: str = request.form.get('user_id')
    type: str = request.form.get('command')
    text: str = request.form.get('text')
    print(request.form)

    if type == '/mokuhyo':
        print(text)

    blocks = [
        blockkit.section('今日の目標は達成できたかな？'),
        # blockkit.button('できた！', 'True', 'completed'),
        # blockkit.button('できなかった', 'False', 'completed'),
    ]
    json_dict = {
        'response_type': 'in_channel',
        'blocks': blocks
    }

    return jsonify(json_dict)


if __name__ == '__main__':
    app.run()
