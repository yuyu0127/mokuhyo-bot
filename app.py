from flask import Flask, jsonify, request, Response
import json
import blockkit
import slackapi

app = Flask(__name__)


@app.route('/command', methods=['POST'])
def handle_command():
    print(request.form.to_dict())
    workspace_name: str = request.form.get('team_domain')
    user: str = request.form.get('user_id')
    type: str = request.form.get('command')
    text: str = request.form.get('text')

    if type == '/mokuhyo':
        pass

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

    return jsonify(json_dict), 200


@app.route('/interactive', methods=['POST'])
def handle_interactive():
    print(request.form.to_dict())

    text = 'おめでとう！'
    payload = json.loads(request.form.to_dict()['payload'])
    print(payload)
    url = payload['response_url']
    slackapi.post_message_to(url, text=text, response_type='ephemeral')
    return '', 200


if __name__ == '__main__':
    app.run()
