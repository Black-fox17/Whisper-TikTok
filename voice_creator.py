import edge_tts


def create_voice(prompt, voice_id):
    voice_response = edge_tts.create_voice(
        prompt=prompt,
        voice_id=voice_id
    )
    return voice_response
