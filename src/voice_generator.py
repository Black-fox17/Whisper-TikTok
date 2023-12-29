import json

import requests


def generate_voice(prompt, voice_id, key):
    url = "https://modelslab.com/api/v6/voice/text_to_voice"
    headers = {'Content-Type': 'application/json'}
    payload = json.dumps({
        "key": key,
        "prompt": prompt,
        "voice_id": voice_id,
        "webhook": None,
        "track_id": None
    })

    response = requests.post(url, headers=headers, data=payload)
    voice = response.text

    return voice
