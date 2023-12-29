import requests


def generate_image(prompt, negative_prompt, samples, guidance_scale, height, width, num_inference_steps, key):
    url = "https://modelslab.com/api/v6/realtime/text2img"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = f'key={key}&prompt={prompt}&negative_prompt={negative_prompt}&samples={samples}&guidance_scale={guidance_scale}&height={height}&width={width}&num_inference_steps={num_inference_steps}'

    while True:
        response = requests.post(url, headers=headers, data=payload)
        if "wait" not in response.text:
            break

    return response.text
