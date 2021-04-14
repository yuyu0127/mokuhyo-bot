def image(url: str, alt_text: str):
    block = {
        'type': 'image',
        'image_url': url,
        'alt_text': alt_text
    }
    return block


def button(text, value, action_id, style=None):
    block = {
        'type': 'button',
        'action_id': action_id,
        'text': {
            'type': 'plain_text',
            'emoji': True,
            'text': text
        },
        'value': value
    }
    if style:
        block['style'] = style

    return block


def md_text(text):
    block = {
        'type': 'mrkdwn',
        'text': text
    }
    return block


def static_select(placeholder_text: str, options, action_id: str):
    block = {
        "type": "static_select",
        "action_id": action_id,
        "placeholder": {
                "type": "plain_text",
                "text": placeholder_text,
                "emoji": True
        },
        "options": options
    }
    return block


def option(text, value):
    block = {
        "text": {
            "type": "plain_text",
            "text": text,
            "emoji": True
        },
        "value": value
    }
    return block


def section(text, accessory=None):
    block = {
        'type': 'section',
        'text': {
                'type': 'mrkdwn',
                'text': text
        }
    }
    if accessory:
        block['accessory'] = accessory
    return block


def divider():
    block = {
        'type': 'divider'
    }
    return block


def actions(elements):
    block = {
        'type': 'actions',
        'elements': elements
    }
    return block


def context(elements):
    block = {
        'type': 'context',
        'elements': elements
    }
    return block