import json
import os
from datetime import datetime

from flask import Flask, Response, jsonify, request

import blockkit
import db
import slackapi
from localization import l8n

app = Flask(__name__)

__import__('dotenv').load_dotenv()
WEBHOOK_URL = os.environ.get('WEBHOOK_URL')


@app.route('/command', methods=['POST'])
def handle_command():
    '''
    スラッシュコマンドをハンドリングする
    '''
    payload = request.form.to_dict()
    print('[Command Payload]\n', json.dumps(
        payload, ensure_ascii=False, indent=4))

    user_id: str = payload['user_id']
    type: str = payload['command']
    text: str = payload['text']

    if type == '/mokuhyo':
        # DBにデータを登録
        db.register_goal(datetime.now(), user_id, text)

        # 宣言するかの確認ボタンを送信
        blocks = [
            blockkit.section(l8n["confirmDeclare"].format(content=text)),
            blockkit.actions([
                blockkit.button(l8n['declareButton'],
                                'declare', 'True', style='primary'),
                blockkit.button(l8n['notDeclareButton'], 'declare', 'False'),
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
    '''
    ボタンなどへのアクションをハンドリングする
    '''
    payload = json.loads(request.form.to_dict()['payload'])
    print('[Interactive Payload]\n', json.dumps(
        payload, ensure_ascii=False, indent=4))

    resp_url = payload['response_url']
    action = payload['actions'][0]
    act_value = action['value']
    act_id = action['action_id']
    user_id = payload['user']['id']

    # 目標宣言ボタンへの対応に対する処理
    if act_value == 'declare':
        goal = db.fetch_goal(user_id)
        content = goal['content']
        print(goal)

        # 目標を宣言するボタンが押された時
        if act_id == 'True':
            text = l8n['broadcastDeclare'].format(
                user_id=user_id, content=content)
            slackapi.webhook_message(WEBHOOK_URL, text=text)

        # 目標を宣言しないボタンが押された時
        else:
            pass

        # 共通処理としてボタンを消す
        slackapi.respond(
            resp_url, text=l8n['confirmDeclare'].format(content=content), replace_original=True)

    # 目標達成ボタンへの対応に対する処理
    if act_value == 'completed':
        goal = db.fetch_goal(user_id)
        content = goal['content']
        print(goal)

        # 目標達成できたボタンが押された時
        if act_id == 'True':
            # 達成フラグをTrueに設定
            db.set_completed(user_id, True)
            # 達成できたことをチャンネルに投稿
            text = l8n['broadcastDone'].format(
                user_id=user_id, content=content)
            slackapi.webhook_message(WEBHOOK_URL, text=text)

        # 目標達成できなかったボタンが押された時
        else:
            # 達成フラグをFalseに設定
            db.set_completed(user_id, False)

        # 共通処理としてボタンを消す
        slackapi.respond(
            resp_url, text=l8n['confirmDone'].format(content=content), replace_original=True)

    return '', 200


if __name__ == '__main__':
    app.run()
