import unittest
from unittest.mock import patch

import requests
from main import create_voice, generate_images


class TestMainFunctions(unittest.TestCase):

    @patch('requests.post')
    def test_generate_images(self, mock_post):
        mock_response = requests.Response()
        mock_response.status_code = 200
        mock_response._content = b'{"status": "done", "images": ["image1", "image2"]}'
        mock_post.return_value = mock_response

        response = generate_images(
            prompt='A serene beach at sunset',
            negative_prompt='low quality',
            samples=4,
            guidance_scale=7.5,
            height=1080,
            width=1920,
            num_inference_steps=50
        )
        self.assertEqual(response['status'], 'done')
        self.assertEqual(len(response['images']), 2)

    @patch('requests.post')
    def test_create_voice(self, mock_post):
        mock_response = requests.Response()
        mock_response.status_code = 200
        mock_response._content = b'{"status": "done", "audio": "audio_file"}'
        mock_post.return_value = mock_response

        response = create_voice(
            prompt='Welcome to Whisper-TikTok tutorial',
            voice_id='jack_sparrow'
        )
        self.assertEqual(response['status'], 'done')
        self.assertEqual(response['audio'], 'audio_file')

if __name__ == '__main__':
    unittest.main()
