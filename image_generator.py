"""
This file contains the function for generating images using the Modelslab API.
"""
import requests


def generate_images(prompt, negative_prompt, samples, guidance_scale, height, width, num_inference_steps):
    """
    Generates images based on the provided prompt and parameters.

    :param prompt: The prompt for the image generation.
    :param negative_prompt: The negative prompt for the image generation.
    :param samples: The number of samples to generate.
    :param guidance_scale: The scale of guidance for the generation.
    :param height: The height of the generated image.
    :param width: The width of the generated image.
    :param num_inference_steps: The number of inference steps for the generation.
    :return: The response from the image generation API.
    """
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
