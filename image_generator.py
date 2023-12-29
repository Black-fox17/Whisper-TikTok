import requests


def generate_images(prompt, negative_prompt, samples, guidance_scale, height, width, num_inference_steps):
    url = 'https://modelslab.com/api/v6/realtime/text2img'
    payload = {
        'prompt': prompt,
        'negative_prompt': negative_prompt,
        'samples': samples,
        'guidance_scale': guidance_scale,
        'height': height,
        'width': width,
        'num_inference_steps': num_inference_steps
    }
    response = requests.post(url, json=payload)
    while response.json().get('status') == 'wait':
        response = requests.post(url, json=payload)
    return response.json()
