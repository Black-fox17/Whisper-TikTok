import streamlit as st
from src.image_generator import generate_image
from src.video_creator import create_video
from src.voice_generator import generate_voice

st.title('Whisper-TikTok Configuration')

api_key = st.text_input('API Key')
num_images = st.number_input('Number of Images', min_value=1)
text_prompt = st.text_input('Text Prompt for TTS')
engine = st.selectbox('Engine', ['API', 'Built-in'])

if st.button('Submit'):
    image_response = generate_image(
        prompt=text_prompt,
        negative_prompt='low quality',
        samples=num_images,
        guidance_scale=7.5,
        height=1920,
        width=1080,
        num_inference_steps=50,
        key=api_key
    )
    while image_response.get('status') == 'wait':
        image_response = generate_image(
            prompt=text_prompt,
            negative_prompt='low quality',
            samples=num_images,
            guidance_scale=7.5,
            height=1920,
            width=1080,
            num_inference_steps=50,
            key=api_key
        )
    st.image(image_response.get('images'))

    voice_response = generate_voice(
        prompt=text_prompt,
        voice_id='voice_example_id',
        key=api_key
    )
    st.audio(voice_response.get('voice'))

    video_response = create_video(image_response.get('images'), voice_response.get('voice'))
    st.video(video_response.get('video'))
