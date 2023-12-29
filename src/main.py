from . import streamlit_app
from .image_generator import generate_image
from .video_creator import create_video
from src.voice_generator import generate_voice


def main():
    streamlit_app.start()

if __name__ == "__main__":
    main()
