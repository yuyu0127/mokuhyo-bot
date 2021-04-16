import json
import os

import requests


def post_message(url, **kwargs):
    payload = kwargs
    print(url, payload)
    return requests.post(url, data=json.dumps(payload).encode('utf8'), headers={'Content-Type': 'application/json'})


def post_text(url, text):
    return post_message(url, text=text)


def post_blocks(url, blocks):
    return post_message(url, blocks=blocks)
