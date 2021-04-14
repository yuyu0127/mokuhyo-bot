import json
import os
from xml.sax.saxutils import escape
from urllib.parse import quote

import requests

WEBHOOK_URL = os.environ.get('WEBHOOK_URL')


def post_message(**kwargs):
    url = WEBHOOK_URL
    payload = kwargs
    print(payload)
    return requests.post(url, data=json.dumps(payload).encode('utf8'), headers={'Content-Type': 'application/json'})

def post_text(text):
    return post_message(text=text)

def post_blocks(blocks):
    return post_message(blocks=blocks)