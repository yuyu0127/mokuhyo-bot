import json
import os

import requests

XOXB_TOKEN = os.environ.get('XOXB_TOKEN')


def webhook_message(url, **kwargs):
    payload = kwargs
    print(url, payload)
    return requests.post(url, data=json.dumps(payload).encode('utf8'), headers={'Content-Type': 'application/json'})


def webhook_text(url, text):
    return webhook_message(url, text=text)


def webhook_blocks(url, blocks):
    return webhook_message(url, blocks=blocks)


def post_direct_message(user_id, **kwargs):
    channel_id = fetch_im_channel_id(user_id)
    url = '	https://slack.com/api/chat.postMessage'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + XOXB_TOKEN
    }
    payload = {
        'channel': channel_id
    }
    return requests.post(url, data=json.dumps(payload).encode('utf8'), headers=headers)


def fetch_im_channel_id(user_id):
    url = 'https://slack.com/api/conversations.open'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + XOXB_TOKEN
    }
    payload = {
        'users': [user_id]
    }
    res = requests.post(url, data=json.dumps(
        payload).encode('utf8'), headers=headers)
    id = res['channel']['id']
    return id
