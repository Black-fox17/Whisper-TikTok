"""
This file contains the function for generating voice audio using the Microsoft Edge Text-to-Speech API.
"""
import edge_tts


def create_voice(prompt, voice_id):
    """
    Generates voice audio from a given prompt and selected voice_id.

    :param prompt: The text prompt to generate the speech from.
    :param voice_id: The identifier for the chosen voice model.
    :return: A dictionary containing the response from the voice generation API.
    """
    voice_response = edge_tts.create_voice(
        prompt=prompt,
        voice_id=voice_id
    )
    return voice_response
