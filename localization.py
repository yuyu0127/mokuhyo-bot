import json

l8n: dict[str, str] = {}
with open('l8n.json', encoding='utf8') as f:
    l8n = json.load(f)
