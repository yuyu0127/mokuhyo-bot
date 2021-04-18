import json
import os

import requests

__import__('dotenv').load_dotenv()
XOXB_TOKEN = os.environ.get('XOXB_TOKEN')


def webhook_message(url, **kwargs):
    payload = kwargs
    print(url, payload)
    return requests.post(url, data=json.dumps(payload).encode('utf8'), headers={'Content-Type': 'application/json;charset=UTF-8'})


def webhook_text(url, text):
    return webhook_message(url, text=text)


def webhook_blocks(url, blocks):
    return webhook_message(url, blocks=blocks)


def post_message(channel_id, **kwargs):
    url = '	https://slack.com/api/chat.postMessage'
    headers = {
        'Content-Type': 'application/json;charset=UTF-8',
        'Authorization': 'Bearer ' + XOXB_TOKEN
    }
    payload = {
        'channel': channel_id
    }
    res = requests.post(url, data=json.dumps(
        payload).encode('utf8'), headers=headers)
    return res.json()


def post_direct_message(user_id, **kwargs):
    channel_id = fetch_im_channel_id(user_id)
    return post_message(channel_id)


def fetch_im_channel_id(user_id):
    url = 'https://slack.com/api/conversations.open'
    headers = {
        'Content-Type': 'application/json;charset=UTF-8',
        'Authorization': 'Bearer ' + XOXB_TOKEN
    }
    payload = {
        'users': user_id
    }
    data = json.dumps(payload).encode('utf8')
    res = requests.post(url, data=data, headers=headers)
    res_json = res.json()
    if 'channel' in res_json:
        return res_json['channel']['id']
    raise Exception('DMチャンネルの取得中にエラーが発生しました', res_json)
