from flask import Flask, jsonify, request

import blockkit
import emojigen
import slackapi

app = Flask(__name__)


@app.route('/command', methods=["POST"])
def handle_command():
    print(request.form.to_dict())
    workspace_name: str = request.form.get('team_domain')
    user: str = request.form.get('user_id')
    type: str = request.form.get('command')
    text: str = request.form.get('text')
    if type == '/mokuhyo':
        print(text)

    return 'OK', 200


if __name__ == '__main__':
    app.run()
