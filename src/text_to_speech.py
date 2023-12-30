
import requests
import base64

async def tts(final_text: str, voice: str = "en-US-ChristopherNeural", stdout: bool = False, outfile: str = "tts.mp3", args=None) -> bool:
    endpoint = 'YOUR_ENDPOINT'
    api_key = 'YOUR_API_KEY'

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
    }

    data = {
        'text': final_text,
        'voice': voice,
    }

    response = requests.post(endpoint, json=data, headers=headers)

    if response.status_code == 200:
        audio_data = response.content

        if stdout:
            # If stdout is True, print the audio data to the console
            print(audio_data)
        else:
            # If stdout is False, save the audio data to the specified file
            with open(outfile, 'wb') as audio_file:
                audio_file.write(audio_data)

        return True
    else:
        print(f"Error {response.status_code}: {response.text}")
        return False

# Example usage
text_to_speak = "Hello, this is a test."
await tts(text_to_speak)
